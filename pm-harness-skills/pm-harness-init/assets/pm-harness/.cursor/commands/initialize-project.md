# Initialize Project

目标：

根据 project.yaml 完成项目基础设施建设。

读取：

* project.yaml
* AGENTS.md
* rules/*
* docs/*
* openspec/project.md

执行步骤：

## Step1 创建 Design System

读取：

* rules/ui-design.md

生成：

* src/shared/design-system/tokens/*
* src/shared/ui/*
* src/shared/business/*
* src/shared/templates/*
* src/web/src/styles/globals.css
* tailwind.config.ts
* scripts/validate-design-system.py

更新：

* AGENTS.md

---

## Step2 创建 API Standard

读取：

* rules/api.md

生成：

* src/backend/app/api/*
* src/sdk/*
* docs/03-api-index.md

---

## Step3 创建 Database Standard

读取：

* rules/database.md

生成：

* src/backend/app/models/*
* src/backend/app/repositories/*
* docs/04-database-design.md

---

## Step4 创建 Test Framework

读取：

* rules/testing.md

生成：

* tests/unit/*
* tests/integration/*
* tests/e2e/*

---

## Step5 创建 Docker 基线

读取：

* project.yaml

生成：

* docker-compose.yml
* docker/*
* .env.example

---

## Step6 创建 Sprint-00

创建：

* REQ-0000-build-design-system
* REQ-0000-build-api-standard
* REQ-0000-build-test-standard

生成：

* openspec/changes/*
* iterations/sprint-00/*
