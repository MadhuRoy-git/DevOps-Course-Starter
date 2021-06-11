variable "prefix_name" {
    description = "The prefix name used for all resources in this environment"
    default = "AmericanExpress2_MadhuRoy_ProjectExercise"
}

variable "location" {
    description = "The Azure location where all resources in this deployment should be created"
    default = "uksouth" 
}

variable "CLIENT_ID" {
    description = "The Github Client ID for the Terraform Azure app"
}