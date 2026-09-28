# AWS deployment

## Current deployment

Live: https://archive.snhpinballclub.com/ — verified September 27, 2026.

Stack: `snhpc-website-archive` in `us-east-1`; distribution: `E2B9WQHNSCJAZD`; bucket: `snhpc-website-archive-bucket-uvqanalzyf9y`. GitHub repository variables are configured and the manual deployment workflow has succeeded. See `VERIFICATION.md` for acceptance results.

For future content releases, run **Deploy archive to AWS** on main, then `python3 scripts/check-live.py`. Infrastructure updates must preserve the certificate parameter shown below. The commands in the remaining sections document initial provisioning for recovery/reference.

AWS CLI authentication and Cloudflare dashboard access were used for setup. GitHub deploys use the scoped OIDC role, so no long-lived AWS keys are stored in GitHub. GitHub now emits an immutable repository subject; `GitHubSubject` in the template must match the repository's exact main-branch identity.

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

## 2. Add archive.snhpinballclub.com

1. The confirmed domain is `snhpinballclub.com`, managed in Cloudflare. The initially requested `snhpinball.club` was a different hostname; Joshua corrected it before deployment.
2. Request an ACM public certificate for `archive.snhpinballclub.com` in **us-east-1** and add its DNS validation CNAME at the authoritative DNS provider. Wait for `ISSUED`.
3. Update the stack with `CertificateArn`. If DNS is in Route53, also supply its actual `HostedZoneId`; the stack then creates A and AAAA alias records for the archive only.

```sh
aws cloudformation deploy --region us-east-1 --stack-name snhpc-website-archive \
  --template-file infra/archive.json --capabilities CAPABILITY_IAM \
  --parameter-overrides CertificateArn=arn:aws:acm:us-east-1:049145893448:certificate/00b6875d-2962-4bcf-a073-3fbec3e5c5c7
```

For external DNS, omit `HostedZoneId` and create a CNAME for `archive` pointing to the `CloudFrontDomain` output. Keep the ACM validation CNAME for renewal. Wait for CloudFront's status to become `Deployed` and DNS propagation.

AWS references: [S3 origin access control](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html), [CloudFront certificate requirements](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html).

## 3. Live acceptance before any removal

- Load `https://archive.snhpinballclub.com/` and follow Enter the archived site.
- Check home/slideshow, About Us, Events, Gallery, Menu, Our Games and Merch; inspect images and navigation on desktop and mobile.
- Confirm `/wix_archive` redirects to `/wix_archive/`, and archived directory/extensionless page URLs resolve.
- Confirm a made-up page returns **HTTP 404** with the archive error page; an existing image returns the correct image content type.
- Confirm HTTP redirects to HTTPS and the TLS certificate covers the archive hostname.
- Verify the current website build, live homepage and existing archive links again.
- Record the deployment ID, DNS/TLS results and browser checks in `VERIFICATION.md`.

Only after all checks pass should a separate source-repository change remove the duplicate and arrange old-URL redirects. This repository does not perform that removal.
