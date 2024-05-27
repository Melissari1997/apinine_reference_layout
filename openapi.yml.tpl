openapi: 3.0.1
info:
  title: Eoliann Climate Suite API
  description: |
    Eoliann Climate Suite API gives users a quantitative estimate of each climate risk (currently drought, flood and wildfire) for any asset or geographical location within the covered areas. 
    This documentation describes all of the available API calls and properties of the returned objects.
    ***
    For any assistance request, it is possible to contact Eoliann Customer Support through the following channels:

    - **Request Form:** Contact support through the [following form](https://share-eu1.hsforms.com/1yMh0hU88TjutYoNZHeIo2A2dptkp)
    - **Email:** [support@eoliann.com](mailto:support@eoliann.com)

    Customer support will be available Monday to Friday, 9:00 AM to 6:00 PM (GMT+1)

    Please note that our customer support services will not be available during company-recognized holidays.

    Support requests will be considered by customer support within 2 working days from submission.
    ***
  version: 1.0.0
servers:
  - url: https://${domain_name}/
paths:

  #####################################
  #   Drought
  #####################################

  /drought/v1:
    get:
      summary: drought/v1
      description: Returns a drought risk assessment for an address. The input can be either an `address` or both `lat` and `lon` parameters.
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/address"
        - $ref: "#/components/parameters/x-api-key"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${drought_lambda_uri}
        credentials: ${apinine_resource_drought_role}
      security:
        - apinineApiKey: []
        - apinineAuthorizerv2: []
      responses:
        "200":
          description: ok
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/drought"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"
  /ui/drought/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: Returns a drought assessment for an address.
      description: Optional extended description in Markdown.
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${drought_lambda_uri}
        credentials: ${apinine_resource_drought_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/drought"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  /ui/drought/map/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: Return a geojson map for drought assessment in a point
      description: Optional extended description in Markdown.
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/layer"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${map_drought_lambda_uri}
        credentials: ${apinine_resource_map_drought_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/drought"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  #####################################
  #   Flood
  #####################################

  /flood/v1:
    get:
      summary: flood/v1
      description: Returns a flood risk assessment for an address. The input can be either an `address` or both `lat` and `lon` parameters.
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/address"
        - $ref: "#/components/parameters/x-api-key"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${flood_lambda_uri}
        credentials: ${apinine_resource_flood_role}
      security:
        - apinineApiKey: []
        - apinineAuthorizerv2: []
      responses:
        "200":
          description: ok
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/flood"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  /ui/flood/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: /ui/flood/v1
      description: Returns a flood risk assessment for an address. The input can be either an `address` or both `lat` and `lon` parameters.
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${flood_lambda_uri}
        credentials: ${apinine_resource_flood_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/flood"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  /ui/flood/map/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: Return a geojson map for flood assessment in a point
      description: Optional extended description in Markdown.
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/layer"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${map_flood_lambda_uri}
        credentials: ${apinine_resource_map_flood_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/drought"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  /flood/rcp85/v1:
    get:
      summary: flood/rcp85/v1
      description: Returns a flood RCP 8.5 risk assessment for an address. The input can be either an `address` or both `lat` and `lon` parameters.
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/address"
        - $ref: "#/components/parameters/year"
        - $ref: "#/components/parameters/x-api-key"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${flood_rcp85_lambda_uri}
        credentials: ${apinine_resource_flood_rcp85_role}
      security:
        - apinineApiKey: []
        - apinineAuthorizerv2: []
      responses:
        "200":
          description: ok
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/flood"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  /ui/flood/rcp85/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: Returns a flood RCP 8.5 assessment for an address.
      description: Optional extended description in Markdown.
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/year"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${flood_rcp85_lambda_uri}
        credentials: ${apinine_resource_flood_rcp85_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/flood"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  /ui/flood/rcp85/map/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: Return a geojson map for flood RCP 8.5 assessment in a point
      description: Optional extended description in Markdown.
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/layer"
        - $ref: "#/components/parameters/year"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${map_flood_rcp85_lambda_uri}
        credentials: ${apinine_resource_map_flood_rcp85_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/drought"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  /flood/rcp45/v1:
    get:
      summary: flood/rcp45/v1
      description: Returns a flood RCP 4.5 risk assessment for an address. The input can be either an `address` or both `lat` and `lon` parameters.
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/address"
        - $ref: '#/components/parameters/year'
        - $ref: "#/components/parameters/x-api-key"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${flood_rcp45_lambda_uri}
        credentials: ${apinine_resource_flood_rcp45_role}
      security:
        - apinineApiKey: []
        - apinineAuthorizerv2: []
      responses:
        "200":
          description: ok
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/flood"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"
  /ui/flood/rcp45/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: Returns a flood RCP 4.5 assessment for an address.
      description: Optional extended description in Markdown.
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/year"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${flood_rcp45_lambda_uri}
        credentials: ${apinine_resource_flood_rcp45_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/flood"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  /ui/flood/rcp45/map/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: Return a geojson map for flood RCP 4.5 assessment in a point
      description: Optional extended description in Markdown.
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/layer"
        - $ref: "#/components/parameters/year"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${map_flood_rcp45_lambda_uri}
        credentials: ${apinine_resource_map_flood_rcp45_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/drought"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  /flood/rcp26/v1:
    get:
      summary: flood/rcp26/v1
      description: Returns a flood RCP 2.6 risk assessment for an address. The input can be either an `address` or both `lat` and `lon` parameters.
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/address"
        - $ref: '#/components/parameters/year'
        - $ref: "#/components/parameters/x-api-key"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${flood_rcp26_lambda_uri}
        credentials: ${apinine_resource_flood_rcp26_role}
      security:
        - apinineApiKey: []
        - apinineAuthorizerv2: []
      responses:
        "200":
          description: ok
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/flood"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"
  /ui/flood/rcp26/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: Returns a flood RCP 2.6 assessment for an address.
      description: Optional extended description in Markdown.
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/year"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${flood_rcp26_lambda_uri}
        credentials: ${apinine_resource_flood_rcp26_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/flood"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  /ui/flood/rcp26/map/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: Return a geojson map for flood RCP 2.6 assessment in a point
      description: Optional extended description in Markdown.
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/layer"
        - $ref: "#/components/parameters/year"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${map_flood_rcp26_lambda_uri}
        credentials: ${apinine_resource_map_flood_rcp26_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/drought"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  #################################
  #   Wildfire   
  #################################

  /wildfire/v1:
    get:
      summary: wildfire/v1
      description: Returns a wildfire risk assessment for an address. The input can be either an `address` or both `lat` and `lon` parameters.
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/address"
        - $ref: "#/components/parameters/x-api-key"      
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${wildfire_lambda_uri}
        credentials: ${apinine_resource_wildfire_role}
      security:
        - apinineApiKey: []
        - apinineAuthorizerv2: []
      responses:
        "200":
          description: ok
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/wildfire"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"
  /ui/wildfire/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: Returns a wildfire assessment for an address.
      description: Optional extended description in Markdown.
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${wildfire_lambda_uri}
        credentials: ${apinine_resource_wildfire_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/wildfire"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  /ui/wildfire/map/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: Return a geojson map for wildfire assessment in a point
      description: Optional extended description in Markdown.
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/layer"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${map_wildfire_lambda_uri}
        credentials: ${apinine_resource_map_wildfire_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/drought"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
        "404":
          $ref: "#/components/responses/404NotFound"

  /ui/login:
    get:
      summary: /ui/login
      description: Consume the OAuth2 code to obtain the JWTs
      tags:
       - UI
      parameters:
        - $ref: "#/components/parameters/callbackUri"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${cognito_login_lambda_uri}
        credentials: ${apinine_resource_cognito_login_role}
      responses:
        "302":
          description: "Redirect to Cognito Hosted UI"
          headers:
            Location:
              schema:
                type: string
          content: {}

  /ui/tokens:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: /ui/tokens
      description: Consume the OAuth2 code to obtain the JWTs
      tags:
        - UI
      parameters:
        - $ref: "#/components/parameters/code"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${get_token_lambda_uri}
        credentials: ${apinine_resource_get_token_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/getToken"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"

  /ui/refresh:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    post:
      summary: /ui/refresh
      description: Obtain new Bearer tokens from a refresh token
      tags:
       - UI
      x-amazon-apigateway-request-validator: body-only
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/refreshTokenRequest"
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${refresh_token_lambda_uri}
        credentials: ${apinine_resource_refresh_token_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/refreshTokenResponse"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"

  /ui/user:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
      - UI
      - CORS
      responses:
        200:
          description: Default response for CORS method
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content: {}
      x-amazon-apigateway-integration:
        type: mock
        requestTemplates:
          application/json: "{\"statusCode\": 200}"
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Headers: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
              method.response.header.Access-Control-Allow-Methods: "'GET,OPTIONS'"
              method.response.header.Access-Control-Allow-Origin: "'*'"
    get:
      summary: /ui/user
      description: Returns info about the currently authenticated user
      tags:
      - UI
      x-amazon-apigateway-integration:
        httpMethod: POST
        type: aws_proxy
        uri: ${user_lambda_uri}
        credentials: ${apinine_resource_user_role}
        responses:
          default:
            statusCode: "200"
            responseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
      security:
        # Empty array will attempt to validate as an ID token,
        # whereas if you have one or more values in it it will validate the bearer as an access token
        - apinineCognitoAuthorizer: ["email"]
      responses:
        "200":
          description: ok
          headers:
            Access-Control-Allow-Origin:
              schema:
                type: "string"
            Access-Control-Allow-Methods:
              schema:
                type: "string"
            Access-Control-Allow-Headers:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/flood"
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"

x-amazon-apigateway-request-validators:
  body-only:
    validateRequestBody: true
    validateRequestParameters: false

components:
  #-------------------------------
  # Reusable schemas
  #-------------------------------
  schemas:
    address:
      type: string
      description: Address of the location, in a format compatible with Google Maps search
      example: Via Cristoforo Colombo, 44, 00154 Roma RM, Italy

    lat:
      type: number
      description: Latitude
      minimum: 27
      maximum: 72
      example: 41.86869

    lon:
      type: number
      description: Longitude
      minimum: -22
      maximum: 45
      example: 12.49536

    year:
      type: number
      description: Future year to consider for the RCP assessment
      enum: [2030, 2040, 2050]
      example: 2030

    layer:
      type: string
      description: Name of the map layer to select
      example: water_intensity_rp20y

    code:
      type: string
      description: Code obtained from OAuth2 login redirect
      example: a1b2c245-aaaa-bbbb-11cc-123b45c678c9

    callbackUri:
      type: string
      description: URI for OAuth2 login redirect
      example: https://example.com

    # FLOOD resources
    floodRiskAssessment:
      type: object
      description: flood risk assessment
      additionalProperties:
        $ref: "#/components/schemas/floodRiskSingleRp"
      example:
        return_period_20y:
          intensity:
            water_height: 0.65
          vulnerability: 0.21
        return_period_100y:
          intensity:
            water_height: 0.75
          vulnerability: 0.22
        return_period_200y:
          intensity:
            water_height: 0.78
          vulnerability: 0.23

    floodRiskSingleRp:
      type: object
      required:
        - intensity
        - vulnerability
      properties:
        intensity:
          type: object
          required:
            - water_height
          properties:
            water_height:
              type: number
              minimum: 0
              description: Height of the water in this specific return period
              example: 1.1
        vulnerability:
          type: number
          minimum: 0
          maximum: 1
          description: Probability of ....
          example: 0.296
      example:
        intensity:
          water_height: 1.1
        vulnerability: 0.296

    flood:
      type: object
      required:
        - address
        - lat
        - lon
        - land_use
        - flood_risk_assessment
        - average_annual_loss
        - risk_index
      properties:
        address:
          $ref: "#/components/schemas/address"
        lat:
          $ref: "#/components/schemas/lat"
        lon:
          $ref: "#/components/schemas/lon"
        land_use:
          type: string
          description: Use of land in the area identified
          example: Agriculture
        flood_risk_assessment:
          $ref: "#/components/schemas/floodRiskAssessment"
        average_annual_loss:
          type: object
          properties:
            value:
              type: number
              description: Expected loss per year, expressed as a fraction of the asset value and corresponding to the average vulnerability.
              example: 0.01255
            national_average:
              type: number
              description: National average value of AAL computed for the land use.
              example: 0.00127819
            regional_average:
              type: string
              description: Regional average value of AAL computed for the land use.
              enum: ["Not implemented"]
        risk_index:
          type: integer
          description: Integer class ranging from 0 to 5 and providing a relative estimate of the climate risk under analysis in the area.
          example: 2
        hazard_index:
          type: string
          description: Integer class ranging from 0 to 5 and providing a relative estimate of the intensity of the hazard under analysis in the area.
          enum: ["Not implemented"]

    # DROUGHT resources
    drought:
      type: object
      required:
        - address
        - lat
        - lon
        - drought_risk_assessment
        - risk_index
        - average_annual_loss
        - hazard_index
      properties:
        address:
          $ref: "#/components/schemas/address"
        lat:
          $ref: "#/components/schemas/lat"
        lon:
          $ref: "#/components/schemas/lon"
        drought_risk_assessment:
          $ref: "#/components/schemas/droughtRiskAssessment"
        average_annual_loss:
          type: object
          properties:
            value:
              type: number
              description: Expected loss per year, expressed as a fraction of the asset value and corresponding to the average vulnerability.
              example: 0.01255
            national_average:
              type: number
              description: National average value of AAL computed for the land use.
              example: 0.00127819
            regional_average:
              type: string
              description: Regional average value of AAL computed for the land use.
              enum: ["Not implemented"]
        risk_index:
          type: integer
          description: Integer class ranging from 0 to 5 and providing a relative estimate of the climate risk under analysis in the area.
          example: 2
        hazard_index:
          type: string
          description: Integer class ranging from 0 to 5 and providing a relative estimate of the intensity of the hazard under analysis in the area.
          enum: ["Not implemented"]

    droughtRiskAssessment:
      type: object
      description: drought risk assessment
      additionalProperties:
        $ref: "#/components/schemas/droughtRiskSingleRp"
      example:
        rp_20:
          duration_months: 18.3
          severity: 16
        rp_100:
          duration_months: 27.6
          severity: 24.5
        rp_200:
          duration_months: 31.6
          severity: 28.2

    droughtRiskSingleRp:
      type: object
      required:
        - duration_months
        - severity
      properties:
        duration_months:
          type: number
        severity:
          type: number
      example:
        duration_months: 18.3
        severity: 24.5

    # WILDFIRE resources

    wildfireRiskSingleRp:
      type: object
      required:
        - intensity
        - vulnerability
      properties:
        intensity:
          type: number
        vulnerability:
          type: string
          enum: ["Not implemented"]
      example:
        intensity: 30.33
        severity: "Not implemented"

    wildfireRiskAssessment:
      type: object
      description: wildfire risk assessment
      additionalProperties:
        $ref: "#/components/schemas/wildfireRiskSingleRp"
      example:
        return_period_2y:
          intensity: 30.33
          vulnerability: "Not implemented"
        return_period_10y:
          intensity: 40.96
          vulnerability: "Not implemented"
        return_period_30y:
          intensity: 45.19
          vulnerability: "Not implemented"

    wildfire:
      type: object
      required:
        - address
        - lat
        - lon
        - wildfire_risk_assessment
        - risk_index
        - average_annual_loss
        - hazard_index
      properties:
        address:
          $ref: "#/components/schemas/address"
        lat:
          $ref: "#/components/schemas/lat"
        lon:
          $ref: "#/components/schemas/lon"
        wildfire_risk_assessment:
          $ref: "#/components/schemas/wildfireRiskAssessment"
        average_annual_loss:
          type: object
          properties:
            value:
              type: number
              description: Expected loss per year, expressed as a fraction of the asset value and corresponding to the average vulnerability.
              example: 0.01255
            national_average:
              type: number
              description: National average value of AAL computed for the land use.
              example: 0.00127819
            regional_average:
              type: string
              description: Regional average value of AAL computed for the land use.
              enum: ["Not implemented"]
        risk_index:
          type: integer
          description: Integer class ranging from 0 to 5 and providing a relative estimate of the climate risk under analysis in the area.
          example: 2
        hazard_index:
          type: string
          description: Integer class ranging from 0 to 5 and providing a relative estimate of the intensity of the hazard under analysis in the area.
          enum: ["Not implemented"]
    
    # AUTH resources
    getToken:
      type: object
      required:
        - id_token
        - access_token
        - refresh_token
        - expires
        - token_type
      properties:
        id_token:
          type: string
        access_token:
          type: string
        refresh_token:
          type: string
        expires:
          type: integer
          minimum: 0
          example: 3600
        token_type:
          type: string
          example: Bearer

    refreshTokenRequest:
      type: object
      required:
        - refresh_token
      properties:
        refresh_token:
          type: string

    refreshTokenResponse:
      type: object
      required:
        - id_token
        - access_token
        - expires
        - token_type
      properties:
        id_token:
          type: string
        access_token:
          type: string
        refresh_token:
          type: string
        expires:
          type: integer
          minimum: 0
          example: 3600
        token_type:
          type: string
          example: Bearer
  #-------------------------------
  # Reusable operation parameters
  #-------------------------------
  parameters:
    lon:
      in: query
      name: lon
      schema:
        $ref: "#/components/schemas/lon"
      description: Longitude of the point
      required: true
    x-api-key:
      in: header
      name: x-api-key
      schema:
        type: string
      required: true
    lat:
      in: query
      name: lat
      schema:
        $ref: "#/components/schemas/lat"
      description: Latitude of the point
      required: true
    address:
      in: query
      name: address
      schema:
        $ref: "#/components/schemas/address"
      description: Address of the point
      required: true
    layer:
      in: query
      name: layer
      schema:
        $ref: "#/components/schemas/layer"
      description: Name of the map layer to select
      required: true
    year:
      in: query
      name: year
      schema:
        $ref: "#/components/schemas/year"
      description: Future year to consider for the RCP assessment
      required: true
    code:
      in: query
      name: code
      schema:
        $ref: "#/components/schemas/code"
      description: Code obtained from OAuth2
      required: true
    callbackUri:
      in: query
      name: callback_uri
      schema:
        $ref: "#/components/schemas/callbackUri"
      description: URI to redirect login to
      required: false
  #-------------------------------
  # Reusable responses
  #-------------------------------
  responses:
    400BadRequest:
      description: "Bad Request"
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
                description: Error in query parameters provided by client
                example: "Either 'address' or both 'lat' and 'lon' parameters must be supplied"
    401Unauthorized:
      description: "Unauthorized"
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
                description: Error type
                enum: [Unauthorized]
                example: Unauthorized
            example:
              message: Unauthorized
    403Forbidden:
      description: "Forbidden"
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
                description: Error type
                enum: [Forbidden]
            example:
              message: Forbidden
    404NotFound:
      description: "Not Found"
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
                description: Data not available for the selected point
                example: Data not available for the selected point
  # security schemes
  securitySchemes:
    apinineApiKey:
      name: "x-api-key"
      type: apiKey
      in: header
      x-amazon-apigateway-api-key-source: HEADER
    apinineAuthorizerv2:
      name: apinineAuthorizerv2
      type: apiKey
      in: header
      x-amazon-apigateway-authtype: Custom scheme with corporate claims
      x-amazon-apigateway-authorizer:
        type: request
        authorizerUri: ${authorizer_lambda}
        authorizerCredentials: ${authorizer_credentials}
        authorizerResultTtlInSeconds: 0
        authorizerPayloadFormatVersion: "1.0"
        identitySource: "method.request.header.x-api-key"
    apinineCognitoAuthorizer:
      name: "Authorization"
      type: apiKey
      in: header
      x-amazon-apigateway-authtype: cognito_user_pools
      x-amazon-apigateway-authorizer:
        type: cognito_user_pools
        providerARNs:
          - ${apinine_user_pool}
