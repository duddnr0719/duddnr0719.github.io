---
title: "00. Introduction for Tabular ML"
date: 2026-07-03T12:00:00+09:00
categories: ["LG Aimers"]
draft: false
---

tabular data’s characteristics → columns
- numerical
- categorical
- binary
- datetime
- text(free-form)
- others → images, videos …

tabular data’s feature
- no spatial or sequential structure

missing values → must handle 

pipeline
- data collection: collecting relevant data + combine information from multiple tables + incorporate useful external data + ensure reproducibility(기록)
- exploratory data analysis(EDA): understand the data
- proprocessing: transform raw data into a form ⇒ model can understand/learn ⇒ must use train dataset(not test or etc dataset)
- modeling
- evaluation: use held-out dataset(지금까지 참고하지 않은 데이터셋)
- deployment & monitoring

hyperparameters

train-test dataset
