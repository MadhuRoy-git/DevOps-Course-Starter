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

variable "CLIENT_SECRET" {
    description = "The Github Client Secret for the Terraform Azure app"
}

variable "BOARD_ID" {
    description = "The Board ID for the Terraform Azure app"
    default = "Board123"
}

variable "DOCKER_REGISTRY_SERVER_URL" {
    description = "The Docker Registry URL for the Terraform Azure app"
    default = "https://index.docker.io"
}

variable "DOCKER_USER" {
    description = "The Docker Account User for the Terraform Azure app"
    default = "madhuaxp"
}

variable "DOCKER_PASSWORD" {
    description = "The Docker Account Password for the Terraform Azure app"
}

variable "OAUTHLIB_INSECURE_TRANSPORT" {
    description = "Disable the SSL check for the Terraform Azure app"
    default = "1"
}

variable "MONGO_CONNECTION_URL" {
    description = "MongoDB connection URL for the Terraform Azure app"
}