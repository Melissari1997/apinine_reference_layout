data "aws_iam_policy_document" "assume_role_oidc" {
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
      values   = var.subject_values
    }

  }
}


data "aws_iam_policy_document" "this" {
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
    resources = var.ecr_repositories
  }

  statement {
    effect    = "Allow"
    actions   = ["lambda:UpdateFunctionCode"]
    resources = var.lambda_functions_arn
  }
}

resource "aws_iam_role" "this" {
  name               = var.role_name
  assume_role_policy = data.aws_iam_policy_document.assume_role_oidc.json
}

resource "aws_iam_policy" "this" {
  name   = "${var.role_name}_policy"
  policy = data.aws_iam_policy_document.this.json
}

resource "aws_iam_policy_attachment" "this" {
  name       = var.role_name
  policy_arn = aws_iam_policy.this.arn
  roles      = [aws_iam_role.this.name]
}
