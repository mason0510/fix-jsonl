# fix-jsonl

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/mason0510/fix-jsonl/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)]()

**Claude Code JSONL Repair Tool** - Clean up and fix Claude Code session files

[English](#english) | [中文](#中文) | [日本語](#日本語)

---

## English

### Problem

This tool fixes the issue reported in [anthropics/claude-code#10199](https://github.com/anthropics/claude-code/issues/10199):

> **Session JSONL files become corrupted or bloated**
> - Truncated JSON lines after crashes or force stops (`Ctrl+C`)
> - Excessive `thinking` content consuming disk space (3-10x actual output)
> - Unable to resume sessions due to parse errors

### What is this?

A command-line tool to repair and optimize Claude Code session JSONL files. Claude Code stores conversation history in `.jsonl` files under `~/.claude/projects/`. These files often contain:

- **Thinking content** - AI's internal reasoning process (3-10x larger than actual output)
- **Corrupted JSON** - Truncated lines from crashes or force stops
- **Invalid entries** - Empty lines, control characters

This tool fixes all these issues automatically.

### Requirements

| Item | Version |
|------|---------|
| Platform | macOS |
| Tested on | macOS 15.0 (24A335) |
| Python | 3.8+ |
| Claude Code | 1.0+ |

### Features

| Feature | Description |
|---------|-------------|
| Remove thinking | Strip `thinking` and `redacted_thinking` blocks |
| Auto-fix JSON | Repair truncated, malformed JSON lines |
| Fuzzy search | Find projects by keyword |
| Batch mode | Fix all projects with `--all` |

### Installation

```bash
# Clone
git clone https://github.com/mason0510/fix-jsonl.git
cd fix-jsonl

# Install globally
chmod +x fix-jsonl.py
sudo ln -sf $(pwd)/fix-jsonl.py /usr/local/bin/fix-jsonl

# Or just run directly
python3 fix-jsonl.py <keyword>
```

### Usage

```bash
# Fix by keyword (fuzzy match)
fix-jsonl wechat
fix-jsonl my-project

# Fix all projects
fix-jsonl --all

# Fix specific path
fix-jsonl /path/to/file.jsonl
fix-jsonl ~/.claude/projects/my-project

# Show help
fix-jsonl
```

### Example Output

```
📁 -Users-demo-my-awesome-project
  ✓ session-abc123.jsonl: thinking:15, fixed:2 (954.2KB)
  ✓ session-def456.jsonl: thinking:8 (237.7KB)

==================================================
Fixed: 2 files | Saved: 1.16 MB
```

### Evaluation

| Aspect | Score |
|--------|-------|
| Feature Completeness | 85/100 |
| Practical Value | 95/100 |

**Why 95/100 practical value?**
- Claude's thinking process is often 3-10x longer than actual output
- Removing it significantly saves disk space
- Auto-fix prevents parsing errors in downstream tools

### Roadmap (v3.0)

- [ ] `--dry-run` preview mode
- [ ] `--backup` create `.bak` files
- [ ] `--compress` output to `.gz`
- [ ] `--keep-thinking` fix format only
- [ ] Parallel processing for `--all`

---

## 中文

### 解决的问题

本工具修复 [anthropics/claude-code#10199](https://github.com/anthropics/claude-code/issues/10199) 中报告的问题：

> **会话 JSONL 文件损坏或膨胀**
> - 崩溃或强制停止（`Ctrl+C`）后 JSON 行被截断
> - 过多的 `thinking` 内容占用磁盘空间（是实际输出的 3-10 倍）
> - 由于解析错误无法恢复会话

### 这是什么？

一个用于修复和优化 Claude Code 会话 JSONL 文件的命令行工具。Claude Code 将对话历史存储在 `~/.claude/projects/` 下的 `.jsonl` 文件中。这些文件通常包含：

- **Thinking 内容** - AI 的内部推理过程（比实际输出大 3-10 倍）
- **损坏的 JSON** - 崩溃或强制停止导致的截断行
- **无效条目** - 空行、控制字符

本工具可自动修复所有这些问题。

### 环境要求

| 项目 | 版本 |
|------|------|
| 平台 | macOS |
| 测试环境 | macOS 15.0 (24A335) |
| Python | 3.8+ |
| Claude Code | 1.0+ |

### 功能

| 功能 | 描述 |
|------|------|
| 移除 thinking | 删除 `thinking` 和 `redacted_thinking` 块 |
| 自动修复 JSON | 修复截断、格式错误的 JSON 行 |
| 模糊搜索 | 按关键词查找项目 |
| 批量模式 | 使用 `--all` 修复所有项目 |

### 安装

```bash
# 克隆
git clone https://github.com/mason0510/fix-jsonl.git
cd fix-jsonl

# 全局安装
chmod +x fix-jsonl.py
sudo ln -sf $(pwd)/fix-jsonl.py /usr/local/bin/fix-jsonl

# 或直接运行
python3 fix-jsonl.py <关键词>
```

### 使用方法

```bash
# 按关键词修复（模糊匹配）
fix-jsonl wechat
fix-jsonl my-project

# 修复所有项目
fix-jsonl --all

# 修复指定路径
fix-jsonl /path/to/file.jsonl
fix-jsonl ~/.claude/projects/my-project

# 显示帮助
fix-jsonl
```

### 评估结果

| 维度 | 评分 |
|------|------|
| 功能完整性 | 85/100 |
| 实用价值 | 95/100 |

**为什么实用价值 95/100？**
- Claude 的 thinking 过程通常比实际输出长 3-10 倍
- 移除后可显著节省磁盘空间
- 自动修复可防止下游工具的解析错误

### 路线图 (v3.0)

- [ ] `--dry-run` 预览模式
- [ ] `--backup` 创建 `.bak` 备份文件
- [ ] `--compress` 输出为 `.gz` 压缩文件
- [ ] `--keep-thinking` 仅修复格式不删除 thinking
- [ ] `--all` 模式并行处理

---

## 日本語

### 解決する問題

このツールは [anthropics/claude-code#10199](https://github.com/anthropics/claude-code/issues/10199) で報告された問題を修正します：

> **セッション JSONL ファイルの破損または肥大化**
> - クラッシュや強制終了（`Ctrl+C`）後の JSON 行の切り詰め
> - 過剰な `thinking` コンテンツによるディスク容量の消費（実際の出力の 3-10 倍）
> - パースエラーによりセッションを再開できない

### これは何？

Claude Code セッション JSONL ファイルを修復・最適化するコマンドラインツールです。Claude Code は会話履歴を `~/.claude/projects/` 配下の `.jsonl` ファイルに保存します。これらのファイルには通常以下が含まれます：

- **Thinking コンテンツ** - AI の内部推論プロセス（実際の出力の 3-10 倍のサイズ）
- **破損した JSON** - クラッシュや強制終了による切り詰められた行
- **無効なエントリ** - 空行、制御文字

このツールはこれらすべての問題を自動的に修復します。

### 動作環境

| 項目 | バージョン |
|------|------------|
| プラットフォーム | macOS |
| テスト環境 | macOS 15.0 (24A335) |
| Python | 3.8+ |
| Claude Code | 1.0+ |

### 機能

| 機能 | 説明 |
|------|------|
| thinking 削除 | `thinking` と `redacted_thinking` ブロックを削除 |
| JSON 自動修復 | 切り詰められた、不正な JSON 行を修復 |
| あいまい検索 | キーワードでプロジェクトを検索 |
| バッチモード | `--all` ですべてのプロジェクトを修復 |

### インストール

```bash
# クローン
git clone https://github.com/mason0510/fix-jsonl.git
cd fix-jsonl

# グローバルインストール
chmod +x fix-jsonl.py
sudo ln -sf $(pwd)/fix-jsonl.py /usr/local/bin/fix-jsonl

# または直接実行
python3 fix-jsonl.py <キーワード>
```

### 使い方

```bash
# キーワードで修復（あいまいマッチ）
fix-jsonl wechat
fix-jsonl my-project

# すべてのプロジェクトを修復
fix-jsonl --all

# 特定のパスを修復
fix-jsonl /path/to/file.jsonl
fix-jsonl ~/.claude/projects/my-project

# ヘルプを表示
fix-jsonl
```

### 評価結果

| 観点 | スコア |
|------|--------|
| 機能の完全性 | 85/100 |
| 実用的価値 | 95/100 |

**なぜ実用的価値が 95/100 か？**
- Claude の thinking プロセスは実際の出力の 3-10 倍の長さになることが多い
- 削除することでディスク容量を大幅に節約
- 自動修復により下流ツールでのパースエラーを防止

### ロードマップ (v3.0)

- [ ] `--dry-run` プレビューモード
- [ ] `--backup` `.bak` ファイル作成
- [ ] `--compress` `.gz` 出力
- [ ] `--keep-thinking` フォーマットのみ修復
- [ ] `--all` モードの並列処理

---

## Changelog

### v2.0.0 (2024-12-30)
- Initial public release
- Remove thinking/redacted_thinking content
- Auto-fix corrupted JSON format
- Fuzzy search project directories
- Batch mode with `--all`

## License

MIT License

## Contributing

Pull requests are welcome! Please open an issue first to discuss what you would like to change.

## Related

- [Claude Code Issue #10199](https://github.com/anthropics/claude-code/issues/10199) - The issue this tool addresses
