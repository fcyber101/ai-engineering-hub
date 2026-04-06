workflow:
  rules:
    - if: $CI_COMMIT_BRANCH != "main" && $CI_PIPELINE_SOURCE != "merge_request_event"
      when: never
    - when: always

variables:
  ORACLE_INSTANCE_IP: "92.5.237.201"
  ORACLE_SSH_USER: "ubuntu"

stages:
  - build
  - deploy

# ================= BUILD TEMPLATE =================
.build:
  stage: build
  tags:
    - shell
  variables:
    MICRO_SERVICE: ""
    SERVICE_VERSION: ""
  before_script:
    - echo "=== [BUILD BEFORE_SCRIPT] ==="
    - echo "MICRO_SERVICE     = $MICRO_SERVICE"
    - echo "SERVICE_VERSION   = $SERVICE_VERSION"
    - export IMAGE_NAME="${CI_REGISTRY_IMAGE}/microservice/${MICRO_SERVICE}"
    - export IMAGE_TAG="${SERVICE_VERSION}"
    - echo "FULL IMAGE        = $IMAGE_NAME:$IMAGE_TAG"
  script:
    - echo "=== [BUILD START] ==="
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_NAME:$IMAGE_TAG .
    - docker push $IMAGE_NAME:$IMAGE_TAG
    - echo "✅ BUILD & PUSH SUCCESS → $IMAGE_NAME:$IMAGE_TAG"

build_shopping_cart:
  extends: .build
  variables:
    MICRO_SERVICE: shopping-cart
    SERVICE_VERSION: "1.8"

# ================= DEPLOY TEMPLATE (FIXED + MAX DEBUG) =================
.deploy:
  stage: deploy
  tags:
    - shell
  variables:
    MICRO_SERVICE: ""
    SERVICE_VERSION: ""
    APP_PORT: ""
    PRODUCTS_SERVICE: "products_app"
    SHOPPING_CART_SERVICE: "shopping_cart_app"

  before_script:
    - chmod 400 $ORACLE_SSH_PRIVATE_KEY
    - echo "=== [DEPLOY BEFORE_SCRIPT DEBUG] ==="
    - echo "MICRO_SERVICE          = $MICRO_SERVICE"
    - echo "SERVICE_VERSION        = $SERVICE_VERSION"
    - echo "APP_PORT               = $APP_PORT"
    - echo "PRODUCTS_SERVICE       = $PRODUCTS_SERVICE"
    - echo "SHOPPING_CART_SERVICE  = $SHOPPING_CART_SERVICE"
    - export IMAGE_NAME="${CI_REGISTRY_IMAGE}/microservice/${MICRO_SERVICE}"
    - export IMAGE_TAG="${SERVICE_VERSION}"
    - echo "FULL IMAGE_NAME        = $IMAGE_NAME:$IMAGE_TAG"

  script:
    - echo "=== [SCP docker-compose.yaml] ==="
    - scp -o StrictHostKeyChecking=no -i $ORACLE_SSH_PRIVATE_KEY docker-compose.yaml $ORACLE_SSH_USER@$ORACLE_INSTANCE_IP:~/

    - |
      echo "=== [STARTING SSH DEPLOY] ==="
      ssh -o StrictHostKeyChecking=no -i $ORACLE_SSH_PRIVATE_KEY $ORACLE_SSH_USER@$ORACLE_INSTANCE_IP "
        set -e
        echo '=== [REMOTE SERVER DEBUG START] ==='
        echo 'MICRO_SERVICE          = $MICRO_SERVICE'
        echo 'SERVICE_VERSION        = $SERVICE_VERSION'
        echo 'APP_PORT               = $APP_PORT'
        echo 'PRODUCTS_SERVICE       = $PRODUCTS_SERVICE'
        echo 'SHOPPING_CART_SERVICE  = $SHOPPING_CART_SERVICE'
        echo 'IMAGE_NAME             = $IMAGE_NAME'
        echo 'IMAGE_TAG              = $IMAGE_TAG'

        echo '=== [Docker Login] ==='
        echo '$CI_REGISTRY_PASSWORD' | docker login -u '$CI_REGISTRY_USER' --password-stdin '$CI_REGISTRY' || echo '❌ LOGIN FAILED'

        echo '=== [Network] ==='
        docker network create micro_service || true

        echo '=== [docker-compose.yaml content] ==='
        cat ~/docker-compose.yaml

        echo '=== [docker compose config] ==='
        IMAGE_NAME='$IMAGE_NAME' \
        IMAGE_TAG='$IMAGE_TAG' \
        APP_PORT='$APP_PORT' \
        PRODUCTS_SERVICE='$PRODUCTS_SERVICE' \
        SHOPPING_CART_SERVICE='$SHOPPING_CART_SERVICE' \
        docker compose -p '$MICRO_SERVICE' config

        echo '=== [PULLING IMAGE] ==='
        IMAGE_NAME='$IMAGE_NAME' \
        IMAGE_TAG='$IMAGE_TAG' \
        APP_PORT='$APP_PORT' \
        PRODUCTS_SERVICE='$PRODUCTS_SERVICE' \
        SHOPPING_CART_SERVICE='$SHOPPING_CART_SERVICE' \
        docker compose -p '$MICRO_SERVICE' pull

        echo '=== [DEPLOYING] ==='
        IMAGE_NAME='$IMAGE_NAME' \
        IMAGE_TAG='$IMAGE_TAG' \
        APP_PORT='$APP_PORT' \
        PRODUCTS_SERVICE='$PRODUCTS_SERVICE' \
        SHOPPING_CART_SERVICE='$SHOPPING_CART_SERVICE' \
        docker compose -p '$MICRO_SERVICE' down --remove-orphans || true

        IMAGE_NAME='$IMAGE_NAME' \
        IMAGE_TAG='$IMAGE_TAG' \
        APP_PORT='$APP_PORT' \
        PRODUCTS_SERVICE='$PRODUCTS_SERVICE' \
        SHOPPING_CART_SERVICE='$SHOPPING_CART_SERVICE' \
        docker compose -p '$MICRO_SERVICE' up -d --force-recreate

        echo '=== [DEPLOY FINISHED] ==='
        docker compose -p '$MICRO_SERVICE' ps
        echo '=== [LAST 30 LOGS] ==='
        docker compose -p '$MICRO_SERVICE' logs --tail=30 app || true
        echo '=== [REMOTE SERVER DEBUG END] ==='
      "

  environment:
    name: development
    url: http://$ORACLE_INSTANCE_IP:$APP_PORT

# ================= DEPLOY JOB =================
deploy_shopping_cart:
  extends: .deploy
  variables:
    MICRO_SERVICE: shopping-cart
    SERVICE_VERSION: "1.8"
    APP_PORT: 3002