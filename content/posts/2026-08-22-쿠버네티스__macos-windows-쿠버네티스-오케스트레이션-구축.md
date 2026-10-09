---
weight: 48
title: "macOS-Windows 쿠버네티스 오케스트레이션 구축"
date: 2026-08-22T12:00:00+09:00
categories: ["쿠버네티스"]
draft: false
---

# 구축 목표
- 앞서 공부한 쿠버네티스 복습 및 실습을 위함.
# 구축 환경
### Control Plane (Master Node)
- OS : macOS
- 역할 : 클러스터 관리, 스케줄링
### Worker Node
- OS : Windows
- 역할 : 애플리케이션(Pod) 구동
### Network
- Tailscale : 노드 간 고정 IP(Overlay Network) 제공
## Tailscale을 사용한 이유
- 문제점
  - 일반적인 네트워크에서는 유동 IP 및 NAT 문제로 노드 간 통신이 불안정
    - NAT(Network Address Traslation) : IP 패킷에 적힌 소켓 주소의 포트 숫자와 소스 및 목적지의 IP 주소 등을 재기록하면서 라우터를 통해 네트워크 트래픽을 주고 받는 기술
  - Mac과 Windows가 서로 다른 네트워크 대역에 있을 경우 연결 불가
→ 이러한 이유로 Tailscale을 사용하게 됨.
- 장점
  - 고정 IP : 각 노드에 고정된 IP를 할당하여 kubeadm init / join 시 안정적
  - 설정 간소화 : 복잡한 포트 포워딩 작업 없이 보안 터널링을 구축할 수 있음
## Control Plane 구축
1. Tailscale을 사용하여 Network를 묶어야 하기 때문에 Tailscale IP를 확인한다
  ![](/images/bc8842cf4cd3dae6.png)
1. 확인한 IP를 가지고 노드를 초기화한다.
  ![](/images/1a2f557e6b2efdd9.png)
1. 결과를 확인한다.
  1. Master Node가 정상 구동 상태인지
  1. Join Token이 생성 되었는지
  ![](/images/162e8d8d4b9817d0.png)
## Worker Node 구축 및 Join
1. Windows 환경 설정
  1. WSL2를 사용(Windows Subsystem for Linux) → 가상의 Linux 환경 세팅
  1. Tailscale을 통해 할당 받은 IP로 Worker Node init
1. 메모리 swap off
  1. 쿠버네티스는 메모리 swap이 켜져 있으면 실행이 되지 않음 
    ```
    sudo swapoff -a
    ```
  1. kubelet 서비스 상태 확인 및 재시작
    ```
    sudo systemctl status kubelet
    sudo systemctl restart kubelet
    ```
  1. 컨테이너 런타임(Containerd) 설정
    1. 초기 구성 시 SystemCgroup 미설정으로 인한 kubelet 실행 실패
    1. config.toml 초기화 및 Cgroup 드라이버 설정 변경으로 해결
    ```
    sudo containerd config default | sudo tee /etc/containerd/config.toml
    sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml
    sudo systemctl restart containerd
    ```
  1. 클러스터 조인
    1. Master Node에서 join을 할 수 있는 token 생성 후 join 명령어 실행
      1. Master Node에서 token 생성 → kubeadm token create --print-join-command
    1. Worker Node에서 join
      1. sudo … → … 부분에 생성된 join-command 붙여 넣어 실행
    1. Master Node에서 실행
      1. kubectl get nodes → 연결이 잘 되었는지 확인
        ![](/images/41cb7f2e21026623.png)
### → 이 과정을 통해 Kubernetes Orchestration 구축이 완료 되었음. (이기종 간 쿠버네티스 오케스트레이션)
## 구축 완료 테스트
- 기본적인 웹 서버(Nginx)를 Pod로 생성하여 워커 노드에 정상적으로 배포 되는지 확인한다.
### 배포 과정
- Master Node에서 실행
<columns>
<column ratio="100">```yaml
# Nginx 이미지를 사용하여 Pod 실행
kubectl run my-nginx --image=nginx

# Pod가 생성이 되었는지, 어느 노드에 할당이 되었는지 확인
kubectl get pods -o wide
```</column>
<column ratio="100">![](/images/b9080df83abcbdda.png)</column>
</columns>
---
<columns>
<column ratio="100">```yaml
# get svc 명령어를 통해 nginx pod가 실행되는 포트 번호 확인
kubectl get svc

# curl 명령어를 통해 해당 포트로 접속하여 html 구조 확인
curl (ip address)/(port)
```</column>
<column ratio="100">![](/images/463ab4119c76899e.png)
![](/images/aa304624e5e4a079.png)</column>
</columns>
---
# 트러블슈팅 기록
## 1. 노드 연결 및 Kubelet 장애
### Kubelet Connection Refused 및 무한 재시작 문제
- 현상: kubeadm join 시 connection refused 에러 발생. Kubelet 서비스가 activating (auto-restart) 상태로 반복됨.
- 원인: WSL2 재부팅 시 Swap 메모리가 자동 활성화됨. K8s는 Swap 활성 시 구동 불가함.
- 해결: 스왑 비활성화 후 Kubelet 재시작함.
```
sudo swapoff -a
sudo systemctl restart kubelet
```
### 도커 서비스 인식 불가 및 런타임 충돌
- 현상: Unit docker.service not found 에러 발생.
- 원인: WSL2 도커는 Windows의 Docker Desktop을 공유하므로 리눅스 표준 서비스로 등록되지 않음.
- 해결: 도커 대신 쿠버네티스 표준인 containerd를 리눅스 내부에 직접 설치하여 독립 런타임 구축.
### Containerd 설정 및 Cgroup 불일치
- 현상: 런타임 설치 후에도 Kubelet 통신 실패.
- 원인: SystemdCgroup 옵션 비활성화로 커널 자원 관리 방식 불일치.
- 해결: config.toml 초기화 및 SystemdCgroup = true 설정 적용.
```
sudo containerd config default | sudo tee /etc/containerd/config.toml
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml
```
## 2. 네트워크(CNI) 및 공유 마운트 이슈
### 필수 네트워크 도구 누락
- 현상: 사전 검사(Preflight) 이후 네트워크 생성 단계에서 멈춤.
- 원인: WSL Ubuntu 기본 이미지에 socat 및 conntrack 패키지 누락됨.
- 해결: 필수 도구 설치.
```
sudo apt-get update
sudo apt-get install -y socat conntrack
```
### Calico CNI 구동 실패 (shared mount)
- 현상: Calico 파드가 not a shared mount 에러와 함께 중단됨.
- 원인: WSL2 루트 파일 시스템의 마운트 전파 속성이 기본적으로 잠겨 있음.
- 해결: 마운트 공유 잠금 해제 및 인터페이스 강제 지정.
```yaml
sudo mount --make-rshared /
kubectl set env daemonset/calico-node -n kube-system IP_AUTODETECTION_METHOD=interface=eth0
```
