openapi: 3.0.1
info:
  title: Eoliann API v1
  description: Eoliann risks API
  version: 1.0.0
servers:
  - url: https://${domain_name}/
paths:

  #####################################
  #   Drought
  #####################################

  /drought/v1:
    get:
      summary: Returns a drought assessment for an address.
      description: Optional extended description in Markdown.
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
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
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
  /ui/drought/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
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
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"

  #####################################
  #   Flood
  #####################################

  /flood/v1:
    get:
      summary: Returns a flood assessment for an address.
      description: Optional extended description in Markdown.
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
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
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"

  /ui/flood/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
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
      summary: Returns a flood assessment for an address.
      description: Optional extended description in Markdown.
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
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"

  /flood/rcp85/v1:
    get:
      summary: Returns a flood RCP 8.5 assessment for an address.
      description: Optional extended description in Markdown.
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
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
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
  /ui/flood/rcp85/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
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
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
  /flood/rcp45/v1:
    get:
      summary: Returns a flood RCP 4.5 assessment for an address.
      description: Optional extended description in Markdown.
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
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
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
  /ui/flood/rcp45/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
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
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
  /flood/rcp26/v1:
    get:
      summary: Returns a flood RCP 2.6 assessment for an address.
      description: Optional extended description in Markdown.
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
        - $ref: "#/components/parameters/year"
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
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
  /ui/flood/rcp26/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
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
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"

  #################################
  #   Wildfire   
  #################################

  /wildfire/v1:
    get:
      summary: Returns a wildfire assessment for an address.
      description: Optional extended description in Markdown.
      parameters:
        - $ref: "#/components/parameters/lat"
        - $ref: "#/components/parameters/lon"
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
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
  /ui/wildfire/v1:
    options:
      summary: CORS support
      description: Enable CORS by allowing all origins
      tags:
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
        "401":
          $ref: "#/components/responses/401Unauthorized"
        "403":
          $ref: "#/components/responses/403Forbidden"
  /ui/login:
    get:
      summary: "Consume the OAuth2 code to obtain the JWTs"
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
      summary: "Consume the OAuth2 code to obtain the JWTs"
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
      summary: "Obtain new Bearer tokens from a refresh token"
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
      summary: Returns info about the currently authenticated user.
      description: Optional extended description in Markdown.
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
      description: Address of ...
      example: Via E. Bugatti, 55, 30016 Jesolo VE, Italy

    lat:
      type: number
      description: Latitude
      minimum: 27
      maximum: 72
      example: 45.55314

    lon:
      type: number
      description: Latitude
      minimum: -22
      maximum: 45
      example: 12.65629

    year:
      type: number
      description: Future year to consider for the RCP assessment
      enum: [2030, 2040, 2050]
      example: 2030

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
        - average_annual_loss
        - risk_index
        - land_use
        - floodRiskAssessment
        - hazard_index
      properties:
        address:
          $ref: "#/components/schemas/address"
        lat:
          $ref: "#/components/schemas/lat"
        lon:
          $ref: "#/components/schemas/lon"
        average_annual_loss:
          type: object
          properties:
            value:
              type: number
              description: something lose something
              example: 0.01255
            national_average:
              type: number
              description: something national
              example: 0.00127819
            regional_average:
              type: string
              description: something regional
              enum: ["Not implemented"]
        risk_index:
          type: integer
          description: very risky!
          example: 2
        land_use:
          type: string
          description: asset identifier
          example: Agriculture
        hazard_index:
          type: string
          description: very hazardous!
          enum: ["Not implemented"]
        elapsed:
          type: number
          description: some time has elapsed!
          example: 4.6357
        floodRiskAssessment:
          $ref: "#/components/schemas/floodRiskAssessment"

    # DROUGHT resources
    drought:
      type: object
      required:
        - address
        - lat
        - lon
        - droughtRiskAssessment
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
        droughtRiskAssessment:
          $ref: "#/components/schemas/droughtRiskAssessment"
        risk_index:
          type: string
          description: very risky!
          enum: ["Not implemented"]
        average_annual_loss:
          type: object
          properties:
            value:
              type: string
              description: something lose something
              enum: ["Not implemented"]
            national_average:
              type: string
              description: something national
              enum: ["Not implemented"]
            regional_average:
              type: string
              description: something regional
              enum: ["Not implemented"]
        hazard_index:
          type: string
          description: very hazardous!
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
      description: wildfire is bad
      additionalProperties:
        $ref: "#/components/schemas/wildfireRiskSingleRp"
      example:
        rp_20:
          intensity: 30.33
          vulnerability: "Not implemented"
        rp_100:
          intensity: 40.96
          vulnerability: "Not implemented"
        rp_200:
          intensity: 45.19
          vulnerability: "Not implemented"

    wildfire:
      type: object
      required:
        - address
        - lat
        - lon
        - wildfireRiskAssessment
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
        wildfireRiskAssessment:
          $ref: "#/components/schemas/wildfireRiskAssessment"
        risk_index:
          type: string
          description: very risky!
          enum: ["Not implemented"]
        average_annual_loss:
          type: object
          properties:
            value:
              type: string
              description: something lose something
              enum: ["Not implemented"]
            national_average:
              type: string
              description: something national
              enum: ["Not implemented"]
            regional_average:
              type: string
              description: something regional
              enum: ["Not implemented"]
        hazard_index:
          type: string
          description: very hazardous!
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

  # security schemese
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
