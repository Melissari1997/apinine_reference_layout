data "aws_iam_policy_document" "gh_authorizer_role_assume_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Federated"
      identifiers = [var.github_oidc_provider]
    }
    actions = ["sts:AssumeRoleWithWebIdentity"]

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:eoliann-dev/*"]
    }

  }
}


data "aws_iam_policy_document" "gh_authorizer_permissions" {
  statement {
    effect    = "Allow"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "ecr:BatchGetImage",
      "ecr:BatchCheckLayerAvailability",
      "ecr:CompleteLayerUpload",
      "ecr:DescribeImages",
      "ecr:DescribeRepositories",
      "ecr:GetDownloadUrlForLayer",
      "ecr:InitiateLayerUpload",
      "ecr:ListImages",
      "ecr:PutImage",
      "ecr:UploadLayerPart"
    ]
    resources = [aws_ecr_repository.apinine_authorizer.arn]
  }

  statement {
    effect    = "Allow"
    actions   = ["lambda:UpdateFunctionCode"]
    resources = [module.apinine_authorizer.lambda_function_arn]
  }

}

resource "aws_iam_role" "gh_authorizer" {
  name               = "gh_authorizer"
  assume_role_policy = data.aws_iam_policy_document.gh_authorizer_role_assume_policy.json
}

resource "aws_iam_policy" "gh_authorizer_policy" {
  name   = "gh_authorizer_policy"
  policy = data.aws_iam_policy_document.gh_authorizer_permissions.json
}

resource "aws_iam_policy_attachment" "gh_authorizer" {
  name       = "gh_authorizer"
  policy_arn = aws_iam_policy.gh_authorizer_policy.arn
  roles      = [aws_iam_role.gh_authorizer.name]
}
