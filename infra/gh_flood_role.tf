data "aws_iam_policy_document" "gh_flood_role_assume_policy" {
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


data "aws_iam_policy_document" "gh_flood_permissions" {
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
    resources = [aws_ecr_repository.apinine_flood.arn]
  }

  statement {
    effect    = "Allow"
    actions   = ["lambda:UpdateFunctionCode"]
    resources = [module.apinine_flood.lambda_function_arn]
  }
}

resource "aws_iam_role" "gh_flood" {
  name               = "gh_flood"
  assume_role_policy = data.aws_iam_policy_document.gh_flood_role_assume_policy.json
}

resource "aws_iam_policy" "gh_flood_policy" {
  name   = "gh_flood_policy"
  policy = data.aws_iam_policy_document.gh_flood_permissions.json
}

resource "aws_iam_policy_attachment" "gh_flood" {
  name       = "gh_flood"
  policy_arn = aws_iam_policy.gh_flood_policy.arn
  roles      = [aws_iam_role.gh_flood.name]
}
