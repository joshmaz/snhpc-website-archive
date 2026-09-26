# AWS deployment

## Access needed

Joshua must provide an authenticated AWS session in the intended account (prefer AWS SSO/profile login; do not paste secret keys into chat), plus access to DNS for `snhpinball.club`. This environment currently has no AWS credentials or profiles. GitHub source-repository secrets exist but cannot be read or safely reused for a separate bucket.

The CloudFormation template provisions a new private, encrypted, versioned S3 bucket, a separate CloudFront distribution with origin access control, a routing function, noindex response headers, and an IAM role scoped only to this archive. It does not modify the production bucket or distribution. The bucket is retained on stack deletion. AWS hosting charges apply.

It expects an existing GitHub OIDC provider at `token.actions.githubusercontent.com` in the account, as used by the source deployment. Confirm it exists before creating the stack; create that provider if this is a different account.

## 1. Provision and publish on CloudFront

From this repository with AWS credentials configured:

```sh
aws sts get-caller-identity
aws cloudformation validate-template --template-body file://infra/archive.json
aws cloudformation deploy --region us-east-1 --stack-name snhpc-website-archive \
  --template-file infra/archive.json --capabilities CAPABILITY_IAM
aws cloudformation describe-stacks --region us-east-1 \
  --stack-name snhpc-website-archive --query 'Stacks[0].Outputs'
```

Set these GitHub Actions **repository variables** on `joshmaz/snhpc-website-archive` from stack outputs:

- `AWS_REGION`: `us-east-1`
- `AWS_ROLE_ARN`: `DeployRoleArn`
- `S3_BUCKET`: `BucketName`
- `CLOUDFRONT_DISTRIBUTION_ID`: `DistributionId`

Run the **Deploy archive to AWS** workflow on main. It builds, validates, syncs only `dist/`, and invalidates only the archive distribution. Deployment is manual to avoid unintended publishing during setup. The role trusts only this repository's main branch. Do not put the current website's bucket or role in these variables.

## 2. Add archive.snhpinball.club

1. Confirm the domain registration and authoritative DNS provider. At preparation time the public DNS query for `archive.snhpinball.club` returned NXDOMAIN; local resolution of `snhpinball.club` also failed. Investigate the parent domain before creating records.
2. Request an ACM public certificate for `archive.snhpinball.club` in **us-east-1** and add its DNS validation CNAME at the authoritative DNS provider. Wait for `ISSUED`.
3. Update the stack with `CertificateArn`. If DNS is in Route53, also supply its actual `HostedZoneId`; the stack then creates A and AAAA alias records for the archive only.

```sh
aws cloudformation deploy --region us-east-1 --stack-name snhpc-website-archive \
  --template-file infra/archive.json --capabilities CAPABILITY_IAM \
  --parameter-overrides CertificateArn=YOUR_VALIDATED_CERTIFICATE_ARN HostedZoneId=YOUR_ZONE_ID
```

For external DNS, omit `HostedZoneId` and create a CNAME for `archive` pointing to the `CloudFrontDomain` output. Keep the ACM validation CNAME for renewal. Wait for CloudFront's status to become `Deployed` and DNS propagation.

AWS references: [S3 origin access control](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html), [CloudFront certificate requirements](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html).

## 3. Live acceptance before any removal

- Load `https://archive.snhpinball.club/` and follow Enter the archived site.
- Check home/slideshow, About Us, Events, Gallery, Menu, Our Games and Merch; inspect images and navigation on desktop and mobile.
- Confirm `/wix_archive` redirects to `/wix_archive/`, and archived directory/extensionless page URLs resolve.
- Confirm a made-up page returns **HTTP 404** with the archive error page; an existing image returns the correct image content type.
- Confirm HTTP redirects to HTTPS and the TLS certificate covers the archive hostname.
- Verify the current website build, live homepage and existing archive links again.
- Record the deployment ID, DNS/TLS results and browser checks in `VERIFICATION.md`.

Only after all checks pass should a separate source-repository change remove the duplicate and arrange old-URL redirects. This repository does not perform that removal.
