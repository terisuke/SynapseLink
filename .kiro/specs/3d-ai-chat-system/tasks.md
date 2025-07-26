# Implementation Plan

## Overview

この実装計画は、ChatdollKitベースの3D AIチャットシステムを段階的に構築するための具体的なコーディングタスクを定義します。各タスクは独立して実行可能で、テスト駆動開発を重視し、継続的な統合を可能にする設計となっています。

## Implementation Tasks

### Phase 0: Core Functionality Prototyping & Setup

- [ ] 0.1 プロジェクト基盤とCI/CDパイプラインの構築
  - Python/FastAPIとUnityのプロジェクト構造を作成し、GitHubリポジトリを初期化する
  - Docker設定ファイルと基本的な依存関係を定義する
  - GitHub Actionsで基本的なCI/CDパイプライン（Lint, テスト実行）を構築する
  - _Requirements: 4.1, 4.4, 17.4, 20.1, 20.2_

- [ ] 0.2 最小限のAPIとUnityクライアントの実装
  - 固定のレスポンスを返すだけの、ごく単純な/api/v1/conversationエンドポイントをFastAPIで実装する
  - Unity側で、このAPIを呼び出し、結果をコンソールに表示するだけの最小限のクライアントを実装する
  - _Requirements: 1.2, 5.1_

- [ ] 0.3 エンドツーエンドの疎通確認
  - UnityクライアントからバックエンドAPIを呼び出し、レスポンスが返ってくるまでの最も単純なエンドツーエンドの疎通を確認する
  - _Requirements: 17.2_

### Phase 1: Foundation and Core Backend

- [ ] 1.1 データベースとストレージ基盤の実装
  - 設計書のSQLスキーマを実装し、Alembicでマイグレーション機能を構築する
  - Supabaseクライアントと基本的なデータアクセス層（リポジトリパターン）を実装する
  - Qdrantとの接続を実装し、文書のEmbedding生成とベクトル保存の基本機能を作成する
  - _Requirements: 3.2, 3.5, 18.3, 2.1_

- [ ] 1.2 基本的なLangChainエージェントの実装
  - ReceptionAgentOrchestratorクラスを作成し、固定のプロンプトで動作する基本エージェントを実装する
  - 会話履歴を保持するための基本的なメモリ管理機能を実装する
  - _Requirements: 4.3, 6.1, 6.2_

- [ ] 1.3 データベースツールの実装
  - SupabaseMCPToolクラスを作成し、来訪者情報の検索や更新を行うツールを実装する
  - エージェントがこのツールを呼び出せるように統合する
  - _Requirements: 12.1, 12.2, 8.1_

### Phase 2: Frontend-Backend Integration and Basic Interaction

- [ ] 2.1 Unityフロントエンドプロジェクトの初期化とChatdollKit連携
  - Unity 2022.3 LTSプロジェクトを作成する
  - Unity Package Manager (UPM) を使用してGit URL (https://github.com/uezo/ChatdollKit.git) からChatdollKitを導入する
  - VRM Importerを導入し、テスト用のVRMモデルをロードできる状態にする
  - AR Foundation パッケージを追加してクロスプラットフォームXR対応を準備する
  - _Requirements: 1.5, 7.1_

- [ ] 2.2 API接続とデータフォーマットの整合性確認
  - UnityクライアントとバックエンドAPI間のデータモデル（PydanticモデルとC#クラス）を実装し、整合性を取る
  - 認証なしで、テキストメッセージをAPIに送信し、AIからのテキストレスポンスを受け取るフローを実装する
  - _Requirements: 5.1, 17.2_

- [ ] 2.3 VRMキャラクターの基本応答実装
  - IVRMCharacterControllerを実装し、バックエンドから受け取ったテキストをキャラクターに発話させる（リップシンクなし）
  - 簡単な待機アニメーションと応答アニメーションを実装する
  - _Requirements: 1.1, 1.3, 1.5, 6.1_

- [ ] 2.4 2D/ARモード切り替え基盤の実装
  - アプリケーション起動時に2DモードかARモードかを選択できるUIを実装する
  - 2Dモード用のシンプルな背景シーンとカメラ制御を実装する
  - モードに応じて空間認識機能のON/OFFを切り替えるロジックを実装する
  - _Requirements: 7.1_

- [ ] 2. データベースとストレージ基盤の実装
  - PostgreSQLスキーマを作成し、データアクセス層を実装する
  - Vector検索とRAG機能の基盤を構築する
  - _Requirements: 3.2, 3.5, 18.3_

- [ ] 2.1 PostgreSQLスキーマとマイグレーションの実装
  - 設計書のSQLスキーマを実装（visitors, conversations, knowledge_documents, system_config）
  - Alembicを使用したデータベースマイグレーション機能を作成
  - 初期データとテストデータのシードスクリプトを作成
  - _Requirements: 3.2, 18.3_

- [ ] 2.2 Supabaseクライアントとデータアクセス層の実装
  - SupabaseクライアントのPythonラッパークラスを作成
  - CRUD操作のためのリポジトリパターンを実装
  - ローカルとクラウドSupabaseの切り替え機能を実装
  - _Requirements: 3.2, 3.5, 21.2_

- [ ] 2.3 Vector検索とRAG基盤の構築
  - Qdrant vector databaseとの接続を実装
  - 文書のembedding生成とベクトル保存機能を作成
  - 類似度検索とRAG検索機能を実装
  - _Requirements: 3.1, 10.1_

### Phase 3: Core AI and Voice Integration

- [ ] 3.1 Playwright MCPとWeb自動化ツールの実装
  - PlaywrightMCPToolクラスを作成
  - 内部Webアプリケーションとの連携機能を実装
  - 予約システムとカレンダー連携のツールを作成
  - _Requirements: 3.3, 9.2, 12.1_

- [ ] 3.2 プラグイン可能なText-to-Speech (TTS) システムの実装
  - ITextToSpeechServiceインターフェースを定義し、音声合成処理を抽象化する
  - AIVIS TTS連携: 日本語用のデフォルトTTSとしてAivisTTSクラスを実装する
  - ElevenLabs TTS連携: 英語用のデフォルトTTSとしてElevenLabsTTSクラスを実装する
  - 管理画面や設定ファイルからTTSプロバイダーを切り替えられる機能を実装する
  - _Requirements: 13.2, 13.3, 1.1_

- [ ] 3.3 音声認識システムの実装
  - 日本語・英語対応の音声認識機能を実装する（Whisper APIや各プラットフォームのネイティブ機能など）
  - 音声入力の品質向上とノイズ除去機能を実装する
  - 言語自動検出と切り替え機能を実装する
  - _Requirements: 13.2, 13.3, 1.1_

### Phase 4: Multimodality and Advanced Tools

- [ ] 4.1 マルチモーダル処理基盤の構築
  - MultimodalProcessorクラスを実装
  - Gemini APIとローカルビジョンモデル（LLaVA等）の統合
  - 画像とテキストの同時処理機能を作成
  - _Requirements: 10.1, 10.2, 11.1_

- [ ] 4.2 文書・ID認識機能の実装
  - OCR機能を使用した文書情報抽出を実装（Tesseract、Google Vision API等）
  - IDカードや名刺の情報抽出機能を作成
  - 抽出データの検証と構造化処理を実装
  - _Requirements: 10.1, 8.3_

### Phase 5: Core Frontend Systems

- [ ] 5.1 REST APIとWebSocket通信の本格実装
  - 会話処理のメインAPIエンドポイントを作成
  - リアルタイム会話のためのWebSocket接続を実装
  - 認証とセキュリティミドルウェア（JWT、MFA）を追加
  - _Requirements: 1.2, 6.1, 15.3, 16.2_

- [ ] 5.2 VRMキャラクター制御システムの高度化
  - ITextToSpeechServiceから取得したAudioClipと同期するリップシンク機能を実装する
  - AIの応答感情に応じて、SetEmotionを呼び出す表情制御を実装する
  - 会話内容に応じた自然なジェスチャー生成システムを作成する
  - _Requirements: 1.1, 1.3, 6.2_

- [ ] 5.3 ジェスチャーと身体アニメーションの実装
  - 会話内容に応じたジェスチャー生成を実装
  - 自然な待機アニメーションシステムを作成
  - カスタムアニメーションの追加機能を実装
  - _Requirements: 1.3, 1.4_

### Phase 6: XR and Spatial Computing (AR Mode)

- [ ] 6.1 AR Foundation基盤のXR空間認識システムの実装
  - ARモードでのみIXRSpatialManagerインターフェースのAR Foundation実装を有効にする
  - AR Plane ManagerとRaycast Managerを活用した空間認識システムを実装する
  - 空間座標系とワールド座標系の変換機能を実装する
  - _Requirements: 7.1, 7.2_

- [ ] 6.2 AR Foundation対応キャラクター配置と追跡システムの実装
  - AR Foundationの平面検出結果を使用した3Dキャラクター配置機能を実装
  - ARAnchorを使用した安定したキャラクター位置固定機能を作成
  - ARCameraを活用したユーザーの位置と視線に応じたキャラクター向き制御を実装
  - 複数ユーザー対応の注意分散システムを実装
  - _Requirements: 7.2, 7.3, 7.5_

- [ ] 6.3 AR Foundation対応空間ジェスチャー認識の実装
  - AR Foundationのハンドトラッキング機能（XR Hands）を統合
  - ARRaycastを使用した指差しや手振りの検出と解釈システムを作成
  - 空間内のオブジェクトやUI要素への指差し認識機能を実装
  - ジェスチャーに応じたキャラクター反応を実装
  - _Requirements: 7.4, 10.3_

### Phase 7: Administration and UI

- [ ] 7.1 受付システム管理インターフェースの実装（Unity UI）
  - IReceptionInterfaceManagerインターフェースを実装
  - 来訪者フォームと予約状況表示機能を作成
  - 施設案内とディレクション表示システムを実装
  - _Requirements: 8.1, 8.4_

- [ ] 7.2 管理者向けWebGUIの実装（React/Vue.js）
  - 知識ベース管理のWebインターフェースを作成（React.js推奨）
  - システム設定とモニタリングダッシュボードを実装
  - TTSプロバイダー切り替えなどのユーザーフレンドリーな設定変更機能を作成
  - _Requirements: 14.1, 14.2, 14.4_

- [ ] 7.3 レポートと分析機能の実装
  - 来訪者統計と利用状況レポート機能を実装
  - 会話ログの分析と品質評価機能を作成
  - データエクスポート（CSV、JSON）と外部システム連携機能を実装
  - _Requirements: 9.4, 19.5_

### Phase 8: Globalization and Finalization

- [ ] 8.1 多言語対応とローカライゼーションの実装
  - Unity Localizationパッケージを使用したUI多言語化を実装
  - 言語別のプロンプトテンプレート管理を実装（日本語・英語）
  - バックエンドAPIレスポンスの多言語対応を作成
  - 言語設定の永続化と同期機能を実装
  - _Requirements: 13.1, 13.2, 13.3, 13.5_

- [ ] 8.2 パフォーマンス最適化とキャッシュシステムの実装
  - Redis統合とマルチレベルキャッシュシステムを実装
  - データベースクエリの最適化とコネクションプーリングを作成
  - AI応答のキャッシュと再利用機能を実装
  - _Requirements: 15.1, 15.5_

- [ ] 8.3 セキュリティとデータ保護機能の実装
  - PII（個人識別情報）のAES-256暗号化を実装
  - AdvancedInputSanitizerクラスを実装
  - 監査ログとセキュリティ監視機能を実装
  - _Requirements: 16.1, 16.3, 16.4_

### Phase 9: Testing, Deployment and Community

- [ ] 9.1 テストスイートと品質保証システムの拡充
  - バックエンドコンポーネントのユニットテスト（pytest）を作成
  - Unity Test Runnerを使用したUnityコンポーネントのテストを実装
  - AIQualityEvaluatorクラスとGolden Datasetを実装
  - API統合テストとE2Eテストスイートを作成
  - _Requirements: 17.1, 17.2, 17.3_

- [ ] 9.2 バックアップとデータ管理システムの実装
  - BackupManagerクラスを実装
  - PostgreSQL/Supabaseの自動バックアップ機能を作成
  - データ復旧とマイグレーション機能を構築
  - GDPR準拠のデータライフサイクル管理を実装
  - _Requirements: 18.3, 18.4, 18.5, 21.2_

- [ ] 9.3 デプロイメントとコンテナ化の実装
  - 全コンポーネントのDockerfile作成
  - docker-compose.yml（開発・本番環境）とKubernetesマニフェストを実装
  - Prometheus/Grafanaによる監視システムを構築
  - 環境別設定管理とシークレット管理を作成
  - _Requirements: 21.1, 21.3, 19.3, 19.4_

- [ ] 9.4 ドキュメントとコミュニティ機能の実装
  - OpenAPI仕様書とSwagger UIを実装
  - 開発者向けドキュメント（README、CONTRIBUTING.md）を作成
  - エンドユーザー向け操作マニュアルを作成
  - Issue/PRテンプレートとセキュリティ開示ポリシーを実装
  - _Requirements: 4.4, 20.1, 20.4, 20.5_

- [ ] 9.5 最終統合とシステムテストの実装
  - 全コンポーネント統合後の動作確認テストを実行
  - 2D/ARモード両方でのエンドツーエンド受付シナリオテストを実施
  - 負荷テスト（Apache JMeter等）とストレステストを実施
  - セキュリティテスト（OWASP ZAP等）と脆弱性評価を実行
  - _Requirements: 15.1, 15.2, 15.3, 17.2, 16.4_

## Implementation Notes

### Development Approach
- **Prototype-First**: まず最もコアな機能を動かすプロトタイプを構築し、リスクを早期に特定
- **Test-Driven Development**: 各機能の実装前にテストケースを作成
- **Incremental Integration**: 小さな機能単位での継続的統合
- **Documentation-First**: コード実装と並行してドキュメント更新

### Task Parallelization (タスクの並行性)
この計画は直線的に見えますが、多くのタスクは並行して進めることが可能です：

- **常に並行**: テスト(12), ドキュメント(15), セキュリティ(11) は、関連する機能開発と常に並行して進める
- **チーム間並行**: フロントエンド(6, 7)とバックエンド(3, 4)のタスクは、APIのインターフェースが合意されていれば、大部分を並行して進めることが可能
- **Phase 2以降**: 基本的な疎通確認後は、複数のフェーズを並行して開発可能

### Task Granularity (タスクの細分化)
各タスク（例: 8.2 管理者向けWebGUIの実装）は、必要に応じてさらに小さなサブタスクに分割して、プロジェクト管理ツール（Jira, GitHub Projectsなど）で追跡することを推奨します。

### Dual-Mode Strategy (2D/AR)
本システムは2Dデスクトップ/キオスクモードと、ARモバイルモードの両方をサポートします：
- **開発初期**: 2Dモードを中心に進め、基本的な対話ロジックを確立
- **AR機能**: Phase 6で集中的に実装（AR Foundation基盤）
- **クロスプラットフォーム対応**: AR FoundationによりiOS/Android/HoloLens等での統一的な開発が可能

### Pluggable Architecture for External Services
TTSなどの外部サービスは、インターフェースを介して抽象化します：
- **デフォルト構成**: AIVIS（日本語）+ ElevenLabs（英語）
- **拡張性**: Google TTS、Amazon Polly等への容易な差し替えが可能
- **設定管理**: 管理画面からのプロバイダー切り替え機能

### Quality Gates
- **Code Coverage**: 最低80%のテストカバレッジを維持
- **Security Scan**: 各PRでセキュリティ脆弱性スキャンを実行
- **Performance Benchmark**: 主要機能のパフォーマンス基準を設定
- **XR Performance**: AR/VR環境での60FPS以上の安定動作を確保

### Risk Mitigation
- **AI Model Fallback**: 外部API障害時のローカルモデル切り替え
- **Data Backup**: 開発中も定期的なデータバックアップを実施
- **Version Control**: 機能ブランチでの開発と慎重なマージプロセス
- **Early Integration Testing**: Phase 0での早期疎通確認によるリスク軽減

### Critical Success Factors
1. **Phase 0の完了**: 基本的な疎通確認が最重要マイルストーン
2. **API設計の合意**: フロントエンド・バックエンド間のインターフェース仕様の早期確定
3. **ChatdollKit統合**: UPMからのGit導入とVRM連携の確実な実装
4. **AR Foundation基盤**: クロスプラットフォームXR機能の安定した基盤構築

この実装計画により、要件と設計で定義された全ての機能を段階的かつ確実に実装することができます。Phase 0のプロトタイピングにより早期にリスクを特定し、並行開発により効率的なプロジェクト進行を実現します。