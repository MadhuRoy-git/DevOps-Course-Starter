terraform {
    backend "azurerm" {
      resource_group_name   = "AmericanExpress2_MadhuRoy_ProjectExercise"
      storage_account_name  = "madhustoreacc"
      container_name        = "madhucontain"
      key                   = "terraform.tfstate"
    }
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = ">=2.49"
        }
    }
}
provider "azurerm" {
    skip_provider_registration = true
    features {}
}
data "azurerm_resource_group" "main" {
    name = "AmericanExpress2_MadhuRoy_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
    name = "terraformed-asp"
    location = var.location
    resource_group_name = var.prefix_name
    kind = "Linux"
    reserved = true

    sku {
        tier = "Basic" 
        size = "B1"
    }
}

resource "azurerm_app_service" "main" {
    name = "madhuterraformhelloapp"
    location = var.location
    resource_group_name = var.prefix_name
    app_service_plan_id = azurerm_app_service_plan.main.id

    site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|madhuaxp/todo-app:latest"
    }

    app_settings = {
    "CLIENT_ID" = var.CLIENT_ID
    "CLIENT_SECRET" = var.CLIENT_SECRET
    "BOARD_ID" = var.BOARD_ID
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "DOCKER_USER" = var.DOCKER_USER
    "DOCKER_PASSWORD" = var.DOCKER_PASSWORD
    "OAUTHLIB_INSECURE_TRANSPORT" = var.OAUTHLIB_INSECURE_TRANSPORT
    "MONGO_CONNECTION_URL" = "mongodb://${azurerm_cosmosdb_account.maindbaccount.name}:${azurerm_cosmosdb_account.maindbaccount.primary_key}@${azurerm_cosmosdb_account.maindbaccount.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
    }
}

resource "azurerm_cosmosdb_account" "maindbaccount" {
  name                = "madhutf-cosmosdb-account"
  resource_group_name = var.prefix_name
  location            = var.location
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "EnableMongo"
  }
  capabilities {
    name = "EnableServerless"
  }
  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 10
    max_staleness_prefix    = 200
  }
  geo_location {
    location          = var.location
    failover_priority = 0
  }
  lifecycle {
    prevent_destroy = false
  }
}

resource "azurerm_cosmosdb_mongo_database" "maindb" {
  name                = "madhutf-cosmos-mongo-db"
  resource_group_name = azurerm_cosmosdb_account.maindbaccount.resource_group_name
  account_name        = azurerm_cosmosdb_account.maindbaccount.name
}

 

