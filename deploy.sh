#!/bin/bash

# BLH Homepage 자동 배포 스크립트
# 사용법: ./deploy.sh [환경]
# 환경: local (기본값), production

set -e

# 설정
DOCKER_IMAGE="wecarmobility/blh-homepage"
CONTAINER_NAME="blh-homepage-container"
PORT="3001"
ENVIRONMENT="${1:-local}"

echo "🚀 BLH Homepage 배포 시작 (환경: $ENVIRONMENT)..."

# 함수 정의
cleanup_containers() {
    echo "🧹 기존 컨테이너 정리 중..."
    if docker ps -q --filter "name=$CONTAINER_NAME" | grep -q .; then
        echo "⏹️  컨테이너 중지 중: $CONTAINER_NAME"
        docker stop $CONTAINER_NAME
    fi
    
    if docker ps -aq --filter "name=$CONTAINER_NAME" | grep -q .; then
        echo "🗑️  컨테이너 제거 중: $CONTAINER_NAME"
        docker rm $CONTAINER_NAME
    fi
}

build_local() {
    echo "🔨 로컬 Docker 이미지 빌드 중..."
    docker build -t $DOCKER_IMAGE:latest .
}

pull_production() {
    echo "📥 프로덕션 Docker 이미지 다운로드 중..."
    docker pull $DOCKER_IMAGE:latest
}

run_container() {
    echo "🔄 새 컨테이너 실행 중..."
    docker run -d \
        --name $CONTAINER_NAME \
        -p $PORT:3001 \
        --restart unless-stopped \
        --health-cmd="curl -f http://localhost:3001/health || exit 1" \
        --health-interval=30s \
        --health-timeout=10s \
        --health-retries=3 \
        -v "$(pwd)/instance:/app/instance" \
        -v "$(pwd)/static/uploads:/app/static/uploads" \
        $DOCKER_IMAGE:latest
}

wait_for_health() {
    echo "⏳ 서비스 시작 대기 중..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:$PORT/health > /dev/null 2>&1; then
            echo "✅ 서비스가 정상적으로 시작되었습니다!"
            return 0
        fi
        
        echo "🔄 헬스체크 시도 $attempt/$max_attempts..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ 서비스 시작에 실패했습니다."
    echo "📋 컨테이너 로그:"
    docker logs $CONTAINER_NAME
    return 1
}

cleanup_images() {
    echo "🧹 사용하지 않는 Docker 이미지 정리 중..."
    docker image prune -f
}

show_status() {
    echo ""
    echo "📊 배포 상태:"
    echo "🌐 접속 URL: http://localhost:$PORT"
    echo "🐳 컨테이너 상태:"
    docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    echo "💡 유용한 명령어:"
    echo "  - 로그 확인: docker logs -f $CONTAINER_NAME"
    echo "  - 컨테이너 중지: docker stop $CONTAINER_NAME"
    echo "  - 컨테이너 재시작: docker restart $CONTAINER_NAME"
}

# 메인 실행 로직
main() {
    # 기존 컨테이너 정리
    cleanup_containers
    
    # 환경에 따른 이미지 준비
    if [ "$ENVIRONMENT" = "local" ]; then
        build_local
    else
        pull_production
    fi
    
    # 컨테이너 실행
    run_container
    
    # 헬스체크 대기
    if wait_for_health; then
        cleanup_images
        show_status
        echo "🎉 배포 완료!"
        exit 0
    else
        echo "❌ 배포 실패!"
        exit 1
    fi
}

# 스크립트 실행
main "$@"