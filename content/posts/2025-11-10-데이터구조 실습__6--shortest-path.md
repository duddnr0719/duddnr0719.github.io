---
title: "6. Shortest Path"
date: 2025-11-10T12:00:00+09:00
categories: ["데이터구조 실습"]
draft: false
---

## 1. 개요
Dijkstra 알고리즘과 Floyd 알고리즘을 사용하여 Shortest Path를 구한다.

### 2. 그래프는 다음과 같다.(주의: 방향 그래프이다)
![](/images/083ea8e67ec62c6e.png)
### 3. \[문제1\] Dijkstra’s Shortest Path 출력
1. 위의 그래프에서 Dijkstra 알고리즘으로 Shortest Path를 생성하는 과정을 출력하여라. 출발 정점은 1이다.
1. Shortest Path 출력이 종료되면 마지막에 최종결과로 Shortest Path의 가중치의 합을 출력한다.
2. 출력하는 화면은 다음과 같다.
\{1\}
0 10 INF 30 100 INF
…
```c
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define TRUE 1
#define FALSE 0
#define MAX_VERTICES    100 
#define INF 1000000 /* 무한대 (연결이 없는 경우) */

typedef struct GraphType {
    int n;  // 정점의 개수
    int weight[MAX_VERTICES][MAX_VERTICES];
} GraphType;

int distance[MAX_VERTICES];/* 시작정점으로부터의 최단경로 거리 */
int found[MAX_VERTICES];        /* 방문한 정점 표시 */

// 방문하지 않은 정점 중 시작 정점으로부터 거리가 짧은 정점을 선택
int choose(int distance[], int n, int found[])
{
    int i, min, minpos;
    min = INT_MAX;
    minpos = -1;
    for (i = 0; i < n; i++)
        if (distance[i] < min && !found[i]) {
            min = distance[i];
            minpos = i;
        }
    return minpos;
}

// 그래프의 가중치 합
int sum_weight(GraphType* g) {
    int sum = 0; // 반드시 초기화
    for (int i = 0; i < g->n; i++) { 
        for (int j = 0; j < g->n; j++) {
            if (g->weight[i][j] < INF) {
                sum += g->weight[i][j]; 
            }
        }
    }
    return sum;
}

// 현재 distance와 found 상태 출력
void print_status(GraphType* g) {
    printf("현재 상태\n");
    printf("정점: ");
    for (int i = 0; i < g->n; i++) printf("%4d", i);
    printf("\n거리: ");
    for (int i = 0; i < g->n; i++) {
        if (distance[i] >= INF) printf("%4s", "INF");
        else printf("%4d", distance[i]);
    }
    printf("\n방문: ");
    for (int i = 0; i < g->n; i++) printf("%4d", found[i]);
    printf("\n\n");
}

void shortest_path(GraphType* g, int start)
{
    int i, u, w;
    for (i = 0; i < g->n; i++) /* 초기화 */
    {
        distance[i] = g->weight[start][i];
        found[i] = FALSE;
    }
    found[start] = TRUE;    /* 시작 정점 방문 표시 */
    distance[start] = 0;
    for (i = 0; i < g->n - 1; i++) {
        print_status(g);
        u = choose(distance, g->n, found);
        if (u == -1) { // 더 이상 도달 가능한 정점이 없으면 종료
            printf("더 이상 선택할 정점이 없습니다. 종료.\n");
            break;
        }
        found[u] = TRUE;
        for (w = 0; w < g->n; w++) {
            if (!found[w]) {
                if (g->weight[u][w] < INF && distance[u] + g->weight[u][w] < distance[w]) {
                    distance[w] = distance[u] + g->weight[u][w];
                }
            }
        }
    }
    // 최종 결과 출력
    printf("최종 최단거리(시작정점 %d):\n", start);
    for (i = 0; i < g->n; i++) {
        if (distance[i] >= INF) printf("정점 %d: INF\n", i);
        else printf("정점 %d: %d\n", i, distance[i]);
    }
}

int main(void)
{
    GraphType g = { 6,
    {{ 0,  10,  INF, 30,  3,  10 },
    { INF,  0,   50, INF, INF ,INF },
    { INF, INF,   0, INF, 10,  5 },
    { INF, INF,  20,  0, INF,  15 },
    { INF, INF,  INF,  60,   0, INF },
    { INF, INF,  INF, INF, INF,  0 }}
    };

    int total = sum_weight(&g);

    shortest_path(&g, 0);
    printf("가중치 총합= %d\n", total);
    
    return 0;
}
```

### 실행 결과
![](/images/7e0933c8673df634.png)

## 4. \[문제2\] Floyd’s Shortest Path 출력
1. 위의 그래프에서 Floyd 알고리즘으로 Shortest Path를 생성하는 과정을 출력하여라.
1. Shortest Path 출력이 종료되면 마지막에 최종결과로 Shortest Path의 가중치의 합을 출력한다.
2. 출력하는 화면은 다음과 같다.
A-1
0 10 INF 30 100 INF
INF 0 50 INF INF INF
…

```c
#include <stdio.h>
#include <stdlib.h>

#define TRUE 1
#define FALSE 0
#define MAX_VERTICES    100 
#define INF 1000000 /* 무한대 (연결이 없는 경우) */

typedef struct GraphType {
    int n;  // 정점의 개수
    int weight[MAX_VERTICES][MAX_VERTICES];
} GraphType;

int A[MAX_VERTICES][MAX_VERTICES];

/* 현재 A 행렬을 화면에 출력 */
void printA(GraphType *g) {
    int i, j;
    printf("===============================\n");
    for (i = 0; i < g->n; i++) {
        for (j = 0; j < g->n; j++) {
            if (A[i][j] == INF)
                printf("  * ");
            else
                printf("%4d ", A[i][j]);
        }
        printf("\n");
    }
    printf("===============================\n");
}

/* A 행렬에 포함된 유한한 가중치 합을 반환 (대각선 제외) */
int sum_weight(GraphType *g) {
    int sum = 0;
    for (int i = 0; i < g->n; i++) {
        for (int j = 0; j < g->n; j++) {
            if (i == j) continue;           /* 대각선(자기 자신)은 제외 */
            if (A[i][j] < INF) sum += A[i][j];
        }
    }
    return sum;
}

void floyd(GraphType* g) {
    int i, j, k;
    for (i = 0; i < g->n; i++)
        for (j = 0; j < g->n; j++)
            A[i][j] = g->weight[i][j];

    printf("초기 A:\n");
    printA(g);
    printf("가중치의 합 = %d\n\n", sum_weight(g));

    /* 중간 정점 k를 이용한 최단거리 갱신 */
    for (k = 0; k < g->n; k++) {
        for (i = 0; i < g->n; i++) {
            for (j = 0; j < g->n; j++) {
                if (A[i][k] == INF || A[k][j] == INF) continue;
                if (A[i][k] + A[k][j] < A[i][j]) {
                    A[i][j] = A[i][k] + A[k][j];
                }
            }
        }
        printf("k = %d 적용 후 A:\n", k);
        printA(g);
        printf("가중치의 합 = %d\n\n", sum_weight(g));
    }
}

int main(void) {
    GraphType g = { 6,
    {{ 0,  10,  INF, 30,  3,  10 },
    { INF,  0,   50, INF, INF ,INF },
    { INF, INF,   0, INF, 10,  5 },
    { INF, INF,  20,  0, INF,  15 },
    { INF, INF,  INF,  60,   0, INF },
    { INF, INF,  INF, INF, INF,  0 }}
    };

    floyd(&g);
    return 0;
}
```

### 실행 결과
<columns>
<column ratio="50">
![](/images/556c7c1d821c595f.png)
</column>
<column ratio="50">
![](/images/a702cdbb750180d2.png)
</column>
</columns>
