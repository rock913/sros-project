技术开发文档：科研智脑 - AI驱动的自动化科学发现平台
文档版本: 2.0 (重大升级)
最后更新: 2025年8月30日
负责人: [您的名字/团队负责人]

1. 项目概述
1.1 升级后的项目目标
本项目旨在将我们现有的full-stack-gitops-on-kubernetes平台，从一个通用的基础设施自动化平台，升级为一个专为自动化科学研究设计的、由自主AI智能体驱动的“科学发现引擎”（代号：“科研智脑”/SciMind）。

最终目标是构建一个能够自主执行完整科研生命周期（从假设生成、文献检索、数据分析、模型训练到报告撰写）的端到端系统，将人类研究员的角色从“执行者”提升为“战略指挥官”。

1.2 升级范围
本次升级的核心是在现有Kubernetes工作负载集群之上，构建三个相互协作的**“能力平面”**：

数据与知识平面 (Data & Knowledge Plane): 负责海量科研数据的存储、处理，并构建动态的、可推理的知识图谱。

模型训练平面 (Model Training Plane): 提供从交互式探索到大规模分布式训练的全套MLOps能力。

智能体运行平面 (Agent Runtime Plane): 作为“大脑”，负责编排和运行多智能体系统，执行复杂的科研工作流。

1.3 升级后的核心技术栈
层面

组件

技术选型 (建议)

作用

基础设施层

虚拟化平台

Proxmox VE 8.x

提供 IaaS 基础



管理/工作负载集群

K3s / K8s (CAPI)

云原生操作系统底座



GPU虚拟化/调度

NVIDIA GPU Operator

将物理GPU资源池化，供K8s调度

数据与知识层

对象存储

MinIO

存储非结构化数据 (PDF, 影像, 模型)



分布式存储

Rook-Ceph

为数据库和应用提供高性能块/文件存储



图数据库

ArangoDB

构建和存储知识图谱



向量数据库

Milvus / Weaviate

支撑RAG和语义检索



数据流水线

Argo Workflows

编排ETL和知识抽取流程

模型训练层

MLOps平台

Kubeflow

提供端到端的模型开发、训练与部署能力

智能体运行层

中央编排框架

LangGraph

作为“主规划智能体”的核心，定义和执行有状态的科研工作流



智能体运行时

K8s Deployments

将每个专业智能体打包为独立的微服务



服务网格

Istio

管理智能体之间的通信、安全和可观测性

2. 升级版架构设计
平台的核心架构演进为在Kubernetes之上构建的、由GitOps统一管理的PaaS层能力。

2.1 架构演进说明
基础设施增强: 原有的工作负载集群现在将通过GitOps自动部署NVIDIA GPU Operator和Rook-Ceph，使其具备了处理大规模数据和AI计算的基础能力。

数据与知识平面: 这是所有智能决策的“原料”来源。Argo CD将在此平面上部署MinIO、ArangoDB和Milvus等核心数据库服务。Argo Workflows将负责运行数据处理和知识抽取的流水线，持续不断地为知识图谱“喂料”。

模型训练平面: Kubeflow的部署为平台提供了强大的MLOps能力。科研人员可以在Jupyter Notebooks中进行探索，并通过Kubeflow Pipelines提交可重复的、可扩展的分布式训练任务，这些任务可以直接利用GPU资源池。

智能体运行平面: 这是系统的“大脑”。一个核心的LangGraph Orchestrator服务负责接收高层指令。它将任务分解后，通过Istio服务网格，调用运行在K8s上的各种专业智能体微服务（如文献智能体、仿真智能体等）来执行具体任务。

3. 实施路线图与任务分解 (V2.0)
我们将采用迭代的方式，逐步为平台添加新的能力。

阶段

目标

预计时间

状态

阶段 0-1

基础设施与自动化大脑就绪

(已完成)

已完成

阶段 2

数据与硬件基础能力构建

2-3 周

未开始

阶段 3

模型训练与知识图谱能力构建

3-4 周

未开始

阶段 4

多智能体系统与端到端工作流

4-6 周

未开始

阶段 2: 数据与硬件基础能力构建
目标: 为平台提供处理大规模数据和运行AI负载的硬件与存储基础。

负责人: [平台团队]

任务 ID

任务描述

依赖

状态

GitOps配置位置

P2-T1

部署 NVIDIA GPU Operator

P1

未开始

platform/hardware/nvidia-gpu-operator/

P2-T2

验证: 提交一个测试Pod，确认可以成功请求并使用GPU资源

P2-T1

未开始

-

P2-T3

部署 Rook-Ceph Operator

P0-T3

未开始

platform/storage/rook-ceph/

P2-T4

通过Rook创建一个Ceph块存储池 (RBD)

P2-T3

未开始

platform/storage/rook-ceph/

P2-T5

部署 MinIO Operator

P1

未开始

platform/storage/minio/

P2-T6

创建一个MinIO租户作为对象存储桶

P2-T5

未开始

platform/storage/minio/

P2-T7

验证: 部署一个测试应用，确认可以动态挂载Ceph和MinIO存储

P2-T4, P2-T6

未开始

-

阶段 3: 模型训练与知识图谱能力构建
目标: 搭建MLOps平台和核心数据库，使平台具备训练模型和构建知识图谱的能力。

负责人: [平台/数据团队]

任务 ID

任务描述

依赖

状态

GitOps配置位置

P3-T1

部署 Kubeflow 核心组件

P2

未开始

apps/ml-platform/kubeflow/

P3-T2

验证: 通过Kubeflow Dashboard启动一个Jupyter Notebook并成功请求GPU

P3-T1

未开始

-

P3-T3

部署 ArangoDB Cluster

P2-T4

未开始

apps/databases/arangodb/

P3-T4

部署 Milvus Cluster

P2-T4

未开始

apps/databases/milvus/

P3-T5

部署 Argo Workflows

P1

未开始

apps/data-pipelines/argo-workflows/

P3-T6

开发第一个知识抽取工作流 (Argo Workflow)

P3-T3, P3-T5

未开始

(新代码库) workflows/

P3-T7

验证: 手动触发工作流，确认能从PDF中提取实体并写入ArangoDB

P3-T6

未开始

-

阶段 4: 多智能体系统与端到端工作流
目标: 部署智能体编排核心，并实现第一个完整的自动化科研工作流。

负责人: [AI/应用团队]

任务 ID

任务描述

依赖

状态

GitOps配置位置

P4-T1

部署 Istio 服务网格

P1

未开始

apps/service-mesh/istio/

P4-T2

开发并容器化 LangGraph Orchestrator 服务

P3

未开始

(新代码库) agents/orchestrator/

P4-T3

开发并容器化第一个专业智能体 (例如：文献检索智能体)

P3

未开始

(新代码库) agents/literature-agent/

P4-T4

将Orchestrator和专业智能体通过GitOps部署到集群

P4-1,2,3

未开始

apps/agent-platform/

P4-T5

集成测试: 通过API调用Orchestrator，触发一个简单的、跨智能体的工作流

P4-T4

未开始

-

P4-T6

端到端工作流开发: 实现“自动化文献综述”的完整流程

P4-T5

未开始

(新代码库) workflows/

P4-T7

最终验证: 提交一个高级科研任务，验证系统能否自主完成并生成报告

P4-T6

未开始

项目核心里程碑

4. 升级后的GitOps仓库策略
为了管理更复杂的系统，Git仓库需要进一步细分：

platform-configs (已有): 保持不变，管理基础设施和核心服务。

application-configs (已有): 保持不变，管理部署在K8s上的应用和服务（包括所有数据库、Kubeflow、智能体服务等）。

workflows-and-pipelines (新增): 专门用于存放Argo Workflows的定义和Kubeflow Pipelines的代码。实现数据/训练流水线即代码。

agents-source-code (新增): 存放所有AI智能体（Orchestrator, 专业智能体）的Python源代码。CI/CD将从此仓库构建容器镜像。

ml-models-source-code (新增): 存放模型训练的源代码和Jupyter Notebooks。

5. 附录：关键设计决策与说明
为什么选择ArangoDB?

如您的文档所述，ArangoDB的原生多模型能力（图、文档）可以让我们在同一个数据库中存储结构化的知识图谱关系和非结构化的源文本元数据，从而简化技术栈，降低运维复杂度。

为什么选择Kubeflow?

Kubeflow是目前在Kubernetes上运行MLOps最成熟、最全面的开源解决方案。它提供了一站式的环境，覆盖了从数据准备、交互式开发、分布式训练到模型服务的全过程，非常适合构建我们的模型训练平面。

LangGraph作为核心的合理性?

科研过程本质上是复杂的、有状态的、且经常包含循环（评估->再搜索->再评估）。LangGraph基于图的、有状态的执行模型，完美契合了这种非线性的科研逻辑，是构建可靠、可控的中央编排框架的最佳选择。