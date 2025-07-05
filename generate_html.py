#!/usr/bin/env python3
"""
HTML Generator for RAG Starter Kit
環境変数を使ってHTMLテンプレートから実際のHTMLファイルを生成
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# プロジェクトディレクトリを取得
PROJECT_DIR = Path(__file__).parent.absolute()

# .envファイルを読み込み
load_dotenv(PROJECT_DIR / ".env")

# config.pyからSERVER_URLを取得
import sys
sys.path.append(str(PROJECT_DIR))
from config import Config

def generate_html():
    """HTMLテンプレートから実際のHTMLファイルを生成"""
    
    # テンプレートファイルのパス
    template_path = PROJECT_DIR / "RAG_demo_template.html"
    output_path = PROJECT_DIR / "RAG_demo.html"
    
    # SERVER_URLを取得
    server_url = Config.SERVER_URL
    
    print(f"🎯 HTML Generator for RAG Starter Kit")
    print(f"📂 Project directory: {PROJECT_DIR}")
    print(f"📝 Template file: {template_path}")
    print(f"📄 Output file: {output_path}")
    print(f"🔗 Server URL: {server_url}")
    
    # テンプレートファイルが存在するかチェック
    if not template_path.exists():
        print(f"❌ Template file not found: {template_path}")
        return False
    
    try:
        # テンプレートファイルを読み込み
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # 環境変数を置き換え
        html_content = template_content.replace('{{SERVER_URL}}', server_url)
        
        # HTMLファイルを出力
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML file generated successfully!")
        print(f"📄 Output: {output_path}")
        print(f"🔗 Server URL configured: {server_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating HTML file: {str(e)}")
        return False

def main():
    """メイン実行関数"""
    success = generate_html()
    
    if success:
        print("\n🎉 HTML generation completed successfully!")
        print("💡 Usage:")
        print("   1. Make sure your .env file contains SERVER_URL=your-server-url")
        print("   2. Run this script to update RAG_demo.html")
        print("   3. Open RAG_demo.html in your browser")
    else:
        print("\n❌ HTML generation failed!")
        print("💡 Make sure:")
        print("   - RAG_demo_template.html exists")
        print("   - .env file contains SERVER_URL")
        print("   - You have write permissions")

if __name__ == "__main__":
    main() 