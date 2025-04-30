#!/bin/bash

# 커밋 메시지 입력 받기
read -p "커밋 메시지를 입력하세요: " user_message

# KST 시간 구하기 (UTC+9)
current_time=$(TZ=Asia/Seoul date "+%Y-%m-%d %H:%M:%S")

# 전체 메시지 구성
commit_message="$user_message | $current_time (KST)"

# Git 명령어 실행
git add .
git commit -m "$commit_message"
git push