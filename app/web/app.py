# PyWebIO 컴포넌트
import os

import yaml
from pywebio import session, config as pywebio_config
from pywebio.input import *
from pywebio.output import *

from app.web.views.About import about_pop_window
from app.web.views.Document import api_document_pop_window
from app.web.views.Downloader import downloader_pop_window
from app.web.views.ParseVideo import parse_video
from app.web.views.Shortcuts import ios_pop_window
from app.web.views.ViewsUtils import ViewsUtils

# 설정 파일 읽기
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.yaml')
with open(config_path, 'r', encoding='utf-8') as file:
    _config = yaml.safe_load(file)

pywebio_config(theme=_config['Web']['PyWebIO_Theme'],
               title=_config['Web']['Tab_Title'],
               description=_config['Web']['Description'])


class MainView:
    def __init__(self):
        self.utils = ViewsUtils()
        self.dark_mode = False

    # 메인 뷰
    def main_view(self):
        # CSS 스타일 정의
        put_html("""
        <style>
        :root {
            --bg-color: #f9f9f9;
            --card-bg: #ffffff;
            --text-color: #333333;
            --primary-color: #4361ee;
            --secondary-color: #3f37c9;
            --accent-color: #4895ef;
            --border-color: #e0e0e0;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        [data-theme="dark"] {
            --bg-color: #121212;
            --card-bg: #1e1e1e;
            --text-color: #e0e0e0;
            --primary-color: #4361ee;
            --secondary-color: #3f37c9;
            --accent-color: #4895ef;
            --border-color: #333333;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            transition: all 0.3s ease;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .dark-mode {
            background-color: var(--bg-color);
            color: var(--text-color);
        }

        .header-container {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: var(--shadow);
        }

        .header-container h1 {
            color: white;
            font-weight: 700;
            margin: 10px 0;
            font-size: 2.5em;
        }

        .header-container p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1em;
        }

        .logo {
            width: 100px;
            height: 100px;
            object-fit: contain;
            transition: transform 0.3s ease;
        }

        .logo:hover {
            transform: scale(1.1);
        }

        .custom-card {
            background-color: var(--card-bg);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: var(--shadow);
            transition: transform 0.3s ease;
        }

        .custom-card:hover {
            transform: translateY(-5px);
        }

        .custom-card-title {
            font-size: 1.5em;
            font-weight: 600;
            margin-bottom: 15px;
            color: var(--primary-color);
        }

        .nav-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
            gap: 15px;
        }

        .nav-btn {
            background-color: var(--card-bg);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .nav-btn:hover {
            background-color: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }

        .action-btn {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            margin-top: 10px;
        }

        .action-btn:hover {
            background-color: var(--secondary-color);
            transform: translateY(-2px);
        }

        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: var(--shadow);
            z-index: 1000;
        }

        select, input {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            background-color: var(--card-bg);
            color: var(--text-color);
            margin-bottom: 15px;
        }

        .feature-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin-top: 20px;
        }

        .feature-card {
            background-color: var(--card-bg);
            border-radius: 10px;
            padding: 20px;
            width: 250px;
            text-align: center;
            box-shadow: var(--shadow);
            transition: transform 0.3s ease;
            border: 1px solid var(--border-color);
        }

        .feature-card:hover {
            transform: translateY(-5px);
        }

        .feature-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
            color: var(--primary-color);
        }

        footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: var(--text-color);
            opacity: 0.7;
            font-size: 0.9em;
        }
        </style>
        """)

        # 메인 영역
        with use_scope('main'):
            # favicon 설정
            favicon_url = _config['Web']['Favicon']
            session.run_js(f"""
                $('head').append('<link rel="icon" type="image/png" href="{favicon_url}">')
            """)

            # footer 제거
            session.run_js("""$('footer').remove()""")

            # referrer 설정
            session.run_js("""$('head').append('<meta name=referrer content=no-referrer>');""")

            # 테마 토글 버튼
            put_html("""
            <div class="theme-toggle" onclick="toggleDarkMode()">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="5"></circle>
                    <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"></path>
                </svg>
            </div>
            """)

            # JavaScript 테마 토글 함수 (직접 JS로 구현)
            session.run_js("""
            function toggleDarkMode() {
                let darkMode = document.body.classList.contains('dark-mode');
                if (!darkMode) {
                    document.body.classList.add('dark-mode');
                    document.documentElement.setAttribute('data-theme', 'dark');
                } else {
                    document.body.classList.remove('dark-mode');
                    document.documentElement.setAttribute('data-theme', 'light');
                }
            }
            """)

            # 헤더 섹션
            put_html(f"""
            <div class="header-container">
                <img src="{favicon_url}" class="logo" alt="logo">
                <h1>TikTok 다운로더</h1>
                <p>워터마크 없이 비디오를 다운로드하세요</p>
            </div>
            """)

            # 네비게이션 바 HTML로 직접 구현
            put_html("""
            <div class="nav-container">
                <button class="nav-btn" onclick="showIosShortcut()">iOS 단축어</button>
                <button class="nav-btn" onclick="showApiDoc()">API 문서</button>
                <button class="nav-btn" onclick="showDownloader()">다운로더</button>
                <button class="nav-btn" onclick="showAbout()">소개</button>
            </div>
            """)

            # 네비게이션 JS 함수
            session.run_js("""
            function showIosShortcut() {
                pywebio.tasks.task_exec('ios_pop_window()');
            }
            function showApiDoc() {
                pywebio.tasks.task_exec('api_document_pop_window()');
            }
            function showDownloader() {
                pywebio.tasks.task_exec('downloader_pop_window()');
            }
            function showAbout() {
                pywebio.tasks.task_exec('about_pop_window()');
            }
            """)

            # 메인 컨텐츠 (div로 구현)
            put_html('<div class="custom-card"><div class="custom-card-title">동영상 다운로드</div>')
            put_text("TikTok 링크를 붙여넣고 다운로드하세요:")
            video_url = input(placeholder="https://vm.tiktok.com/...",
                              required=True, name="video_url")
            put_button("동영상 다운로드", onclick=lambda: parse_video(video_url), color='primary', outline=False)
            put_html("</div>")

            # 기능 카드 섹션
            put_markdown("## 기능")
            put_html("""
            <div class="feature-container">
                <div class="feature-card">
                    <div class="feature-icon">🎬</div>
                    <h3>워터마크 제거</h3>
                    <p>고품질의 워터마크 없는 동영상을 다운로드하세요</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔄</div>
                    <h3>배치 처리</h3>
                    <p>여러 비디오를 한 번에 처리할 수 있습니다</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3>빠른 처리</h3>
                    <p>빠른 서버로 즉시 다운로드할 수 있습니다</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📱</div>
                    <h3>모바일 지원</h3>
                    <p>모든 기기에서 작동합니다</p>
                </div>
            </div>
            """)

            # 추가 옵션 섹션
            options = [
                '🔍 여러 동영상 일괄 다운로드',
                '🔍 사용자 프로필 모든 동영상 다운로드',
                '🎵 음악만 다운로드',
            ]

            put_html('<div class="custom-card"><div class="custom-card-title">추가 기능</div>')
            selected_option = select(
                label="원하는 기능을 선택하세요",
                options=options,
                required=True
            )
            put_button("선택 기능 실행", onclick=lambda: self.handle_option(selected_option), color='primary', outline=False)
            put_html("</div>")

            # 푸터
            put_html("""
            <footer>
                <p>© 2024 TikTok 다운로더 - 개인 사용 목적으로만 사용해주세요</p>
                <p><a href="https://github.com/Evil0ctal/TikTok_Download_API" target="_blank">GitHub 프로젝트</a></p>
            </footer>
            """)

    def handle_option(self, option):
        """선택된 옵션 처리"""
        if '일괄 다운로드' in option:
            parse_video()
        elif '사용자 프로필' in option:
            put_markdown("이 기능은 아직 개발 중입니다. 곧 제공될 예정입니다.")
        elif '음악만 다운로드' in option:
            put_markdown("음악 다운로드 기능은 곧 제공될 예정입니다.")
        else:
            put_markdown("선택한 기능은 현재 사용할 수 없습니다.")
