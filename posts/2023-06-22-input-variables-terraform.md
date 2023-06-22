---
author: Alex Strick van Linschoten
categories:
  - terraform
  - devops
  - softwareengineering
date: "2023-06-22"
description: "All the ways you can set input and local variables when using Terraform."
layout: post
title: "Terraform Input Variables"
toc: true
image: images/inputs-outputs-terraform.png
include-before-body:
  '<script defer data-domain="mlops.systems"
  src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

When working with Terraform code, there are ways to take in user input at the time when you are applying whatever you've defined. To take a perhaps needlessly simple example, you might write a definition that allows you to deploy a new S3 bucket but you probably wouldn't want to hardcode the name of the new bucket; instead, you'd rather take that name at the point of deployment. So if we think of the terraform process as a big function call, our input variables are the inputs we pass into this function application.

There are three main ways that you'll use and encounter input variables in HCL code.

1. variables passed in at the command line using `-var`
2. variables defined in separate files either automatically parsed or passed in using the `-var-file` option at the command line
3. variables defined as environment variables

The first two are fairly commonly used, especially during development / testing, but are not really a great idea if your aim is a production-grade setup. Let's walk through them one by one, but first let's look at the variable block itself in HCL.

## Variable Blocks

A variable block can look like this:

```hcl
variable "some_variable" {
  description = "This is where you describe the variable"
  type        = string
  default     = "ginger_cat"
  nullable    = false
  sensitive   = false
}
```

Most of this is self-explanatory. You can also specify a `validation` value in which you can determine the appropriate or accepted values for the variable. If you set `sensitive` to true, then terraform will (mostly) keep the value out of any output printed in the terminal. The name for the variable should be unique within the module and the value of this variable must be a literal value; it cannot be the result of an expression. If you don't specify a default value then on running `terraform apply` or `plan` you will be asked what value you want to use.

(There are also a limited handful of key words that are forbidden for use as names for the variable; you can look them up [in the docs](https://developer.hashicorp.com/terraform/language/values/variables#declaring-an-input-variable).)

## Variables passed in at the command line

Instead of just waiting for the terraform CLI to ask you what values you want to assign to variables, you can pass them in at the command line. Your variables might live in a `variables.tf` file (or be located across your `.tf` files) but when you run `terraform apply` you can do so in the following way:

```shell
terraform apply -var="some_variable=black_cat"
```

If you have multiple variables (as you are likely to have) then you can use the `-var` option multiple times.

## Variables passed in with files

As you might imagine, this rapidly gets unwieldy so there is also a way to populate a whole file with the variable:value pairs. You can either explicitly specify a filename to use for those variables, or there are certain filenames that will be automatically be loaded in and parsed.

```shell
# passing a file name explicitly
terraform apply -var-file="my_vals.tfvars"
```

A file called `terraform.tfvars`, or `terraform.tfvars.json`, or any file ending in `.auto.tfvars` or `auto.tfvars.json` will all be loaded automatically without the need to explicitly pass them in at the command line.

## Variables passed in using environment variables

Some situations require different approaches than populating a file or passing them in via the command line so terraform also checks any environment variable with the `TF_VAR_` prefix and imports those automatically. For example, we could run:

```shell
export TF_VAR_some_variable=white_cat
```

And the `some_variable` variable would be populated with the `white_cat` value.

## Using variables

You can use variables (to get their values) by using the `var.` prefix. For example, if I was defining an AWS S3 bucket and I wanted to use the value of the `some_variable` value for that bucket name, I could do something like this in my HCL definition:

```hcl
resource "aws_s3_bucket" "my_first_bucket" {
  bucket        = var.some_variable
}
```

## Local variables

Sometimes you want to define local variables that don't need exposing as configurable parameters (as the input variables described above are). We have local variables for this, and you define them in their own block:

```
locals {
  my_cat = "aria"
}
```

The useful thing about local variables is that you *can* assign expressions as the values for these variables, or you can combine or otherwise transform things.

These local variables are accessible elsewhere with the `local.` prefix (e.g. in the above example, as `local.my_cat`)

You might want to use local variables where you have some particular expression that's used multiple times in your file so you want to keep it *DRY* so you use a local variable. Similarly, if something is likely to be changed, you might want to make the change only in one place instead of multiple places. These are only available for use within the module where it is declared and can't be overridden from the outside.

## Variable Precedence

With all these different ways to pass in values for variables, how do you know which one gets chosen? There are precedence rules that determine which value is used. Variables are loaded in this order, and the last one seen is the one that is used:

- environment variables
- the `terraform.tfvars` file
- the `terraform.tfvars.json` file
- any `….auto.tfvars` (or the `.json` equivalent) files
- any `-var` and/or `-var-file` values set via the command line

Nothing about using these variables is particularly difficult to understand, but it's useful to have a sense of those precedence rules nonetheless, especially if you have the same variable defined in multiple places.