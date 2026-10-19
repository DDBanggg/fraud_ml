# ML Roadmap 2026 — Fraud Detection Model v1

**Thời gian:** 19/10/2026–31/12/2026.
**Trạng thái:** Kế hoạch chính thức cho giai đoạn ML, không phải báo cáo kết quả thực nghiệm.

## 1. Project Overview

Real-time Banking Fraud Detection System hướng tới phát hiện gian lận giao dịch ngân hàng theo thời gian thực. Giai đoạn hiện tại là bài tập lớn Machine Learning, tập trung vào batch/offline ML. Định hướng dài hạn là hệ thống Data Engineering với Kafka, Flink và các thành phần liên quan trong đồ án tốt nghiệp HUST kỳ 2027.1.

Tài liệu này cụ thể hóa lịch cuối năm từ [PROJECT_LOG.md](../PROJECT_LOG.md). Phạm vi thuật toán của giai đoạn này được xác định tại đây: chỉ Logistic Regression và XGBoost, dù README và project log trước đó có liệt kê thêm mô hình. Các tài liệu cũ được giữ nguyên để bảo toàn bối cảnh.

## 2. Objectives

Đến 31/12/2026, hoàn thành **Fraud Detection Model v1** với:

- Dataset được lựa chọn và có tài liệu mô tả nguồn, phiên bản, schema, nhãn và điều kiện sử dụng.
- EDA, preprocessing và feature engineering có kiểm soát data leakage.
- Huấn luyện và so sánh đúng hai thuật toán: Logistic Regression baseline và XGBoost mô hình chính.
- Đánh giá Precision, Recall, F1-score, PR-AUC, confusion matrix và False Positive Rate (FPR).
- Chọn classification threshold bằng validation set; đánh giá cuối trên test set độc lập sau khi khóa cấu hình.
- Lưu model artifact, preprocessing pipeline, feature schema và threshold.
- Có hướng dẫn tái lập training và chạy batch inference.

Không đặt trước kết quả benchmark hay cam kết mức metric khi chưa đánh giá dữ liệu. Tiêu chí chọn threshold cần được thống nhất và ghi lại trước final evaluation.

## 3. Scope & Non-goals

**Trong phạm vi:** khảo sát dataset; EDA; chia train/validation/test; preprocessing; features; training hai thuật toán; tuning; class imbalance; threshold selection; error analysis; artifact; batch inference và báo cáo cuối kỳ.

**Ngoài phạm vi đến 31/12/2026:** triển khai Kafka, Flink, API, dashboard, hạ tầng streaming hoặc production deployment. Không thêm thuật toán thứ ba vào kế hoạch chính. Các yêu cầu kế thừa streaming chỉ được tài liệu hóa.

## 4. Dataset Candidates

**Chưa chốt dataset chính thức.** PaySim là ứng viên ưu tiên ban đầu; IEEE-CIS là ứng viên thay thế. Bảng là đánh giá sơ bộ phục vụ lựa chọn, không phải kết quả kiểm tra dữ liệu thực tế. Liên kết từng dòng là nguồn tham khảo; truy cập đầy đủ trên Kaggle có thể cần đăng nhập và chấp nhận điều khoản.

| Dataset / nguồn | Loại bài toán | Đặc điểm dữ liệu | Mức độ phù hợp với ML | Khả năng kế thừa sang streaming | Hạn chế chính |
|---|---|---|---|---|---|
| [PaySim](https://www.kaggle.com/datasets/ealaxi/paysim1) | Transaction fraud trong mobile money mô phỏng | Synthetic; bước thời gian, loại và số tiền giao dịch, bên gửi/nhận, nhãn fraud | Ưu tiên khảo sát cho binary classification và imbalance | Tiềm năng replay theo bước thời gian và xây account history nếu schema đáp ứng | Khác dữ liệu thật; step không phải timestamp đầy đủ; balance fields và biến cảnh báo cần audit leakage |
| [IEEE-CIS Fraud Detection](https://www.kaggle.com/competitions/ieee-fraud-detection/data) | Fraud giao dịch trực tuyến | Transaction và identity nối bằng TransactionID; identity có thể thiếu; TransactionDT là thời gian tương đối | Ứng viên thay thế; tabular ML với preprocessing phức tạp | Có thể khảo sát replay theo TransactionDT; cần xác minh định danh thực thể | Nhiều biến ẩn danh, missing values; không mặc định có account ID ổn định; test công khai thiếu nhãn để tự tính metrics |
| [Credit Card Fraud Detection — ULB](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) | Credit card transaction fraud | Chủ yếu đặc trưng số biến đổi PCA; có Time, Amount và Class | Thuận lợi cho baseline và nghiên cứu imbalance | Có thể khảo sát thứ tự thời gian; hạn chế account history | Thiếu ngữ nghĩa features gốc và account identifiers phục vụ kế thừa; thời gian quan sát ngắn |
| [Bank Account Fraud — Feedzai](https://github.com/feedzai/bank-account-fraud) | Gian lận mở tài khoản ngân hàng | Tabular synthetic từ dữ liệu mở tài khoản đã ẩn danh; temporal dynamics và bias variants | Hữu ích nghiên cứu imbalance, drift và fairness | Có thể kế thừa đánh giá theo thời gian; không mặc định là luồng giao dịch | Đơn vị dự đoán là hồ sơ mở tài khoản, khác transaction fraud; cần giảng viên xác nhận nếu đổi mục tiêu |
| [IBM AML-Data](https://github.com/IBM/AML-Data) | Anti-Money Laundering (AML) | Giao dịch tài chính synthetic với laundering tag | Hữu ích cho AML; không thay thế trực tiếp nhãn transaction fraud | Tiềm năng nghiên cứu lịch sử và quan hệ tài khoản sau khi kiểm tra schema | Nhãn rửa tiền khác fraud; cần kiểm tra điều kiện dữ liệu riêng với license mã nguồn |
| [IBM AMLSim](https://github.com/IBM/AMLSim) | Mô phỏng giao dịch có money laundering patterns | Simulator đa tác tử sinh dữ liệu ngân hàng synthetic | Nguồn mô phỏng AML, cần thêm công chuẩn bị | Có thể nghiên cứu sinh/replay giao dịch và account history ở giai đoạn sau | Là công cụ mô phỏng, cần cấu hình/kiểm tra đầu ra; nhãn AML khác transaction fraud; không xây simulator trong phạm vi chính |

Khả năng streaming trong bảng là cân nhắc thiết kế, phụ thuộc kiểm tra dữ liệu. Không đánh đồng nhãn AML với transaction fraud.

### Cổng quyết định dataset — hạn 01/11/2026

Lập decision record và trao đổi giảng viên dựa trên:

1. Schema, đơn vị quan sát, ý nghĩa nhãn và mức phù hợp với transaction fraud.
2. Timestamp/thời gian tương đối, độ phân giải, thứ tự và account identifiers; không suy diễn transaction ID thành account ID.
3. Missing values, duplicates, fraud rate, chất lượng nhãn, quy mô và tài nguyên tính toán.
4. Thời điểm mỗi trường có sẵn khi dự đoán; audit nhãn, biến cảnh báo, balances và dữ liệu hậu giao dịch. Chỉ dùng feature có bằng chứng khả dụng.
5. Khả năng truy cập, phiên bản, license và điều kiện sử dụng; phân biệt license repository và dataset.
6. Khả năng chia tập có nhãn độc lập và kế thừa features sang streaming.

Tài liệu này không xác nhận đã tải dữ liệu hoặc đã kiểm chứng đầy đủ license. Với IEEE-CIS, cần tạo test nội bộ từ dữ liệu có nhãn thay vì dùng test công khai để tính metrics. Nếu PaySim không đạt, đánh giá IEEE-CIS trước; nếu vẫn chưa phù hợp, ghi blocker và thống nhất với giảng viên, không tự chuyển sang mục tiêu AML.

## 5. Selected ML Algorithms

| Thuật toán | Vai trò | Thiết kế thí nghiệm dự kiến |
|---|---|---|
| Logistic Regression | Baseline | Imputation, encoding, scaling phù hợp; khảo sát regularization và class weighting; chỉ fit trên train |
| XGBoost | Mô hình chính | Khảo sát depth, learning rate, số vòng boosting, regularization và scale_pos_weight; early stopping dùng validation |

Dùng cùng split, feature definitions và quy tắc đánh giá; ghi preprocessing đặc thù từng mô hình. Giới hạn search space và số lần thử theo tài nguyên. Không mặc định XGBoost thắng baseline; kết luận dựa trên đánh giá.

## 6. Weekly Roadmap

Tất cả thời gian thuộc năm 2026. Các deliverables và tiêu chí dưới đây là mục tiêu dự kiến.

| Tuần | Thời gian | Mục tiêu | Công việc cụ thể | Deliverables | Tiêu chí hoàn thành |
|---|---|---|---|---|---|
| 1 | 19–25/10 | ML fundamentals, fraud và imbalance | Học classification, split, metrics, leakage; khảo sát sáu dataset | Ghi chú; bảng khảo sát; checklist lựa chọn | Giải thích FP/FN, PR-AUC và leakage; xác định câu hỏi schema, nhãn và truy cập |
| 2 | 26/10–01/11 | Đánh giá và chốt dataset | Kiểm tra truy cập/điều kiện sử dụng, schema, labels, timestamp, identifiers, leakage; trao đổi giảng viên | Decision record; data dictionary; danh sách trường cần loại/xác minh | Lựa chọn được ghi nhận với nguồn, phiên bản và lý do; nếu bị chặn có phương án thay thế thống nhất với giảng viên |
| 3 | 02–08/11 | EDA và chia dữ liệu | Kiểm tra missing values, duplicates, fraud rate và thời gian; chọn cutoff; khóa test | EDA notebook; split manifest/config | Split tái lập, không trùng record; test cô lập; EDA định hướng mô hình trên train; validation chỉ phục vụ lựa chọn |
| 4 | 09–15/11 | Preprocessing và Logistic Regression baseline | Fit pipeline trên train; train baseline; đánh giá validation với threshold ban đầu ghi rõ | Pipeline; config, seed và baseline metrics | Chạy lại được; đủ metrics bắt buộc; không dùng test chọn cấu hình |
| 5 | 16–22/11 | Feature engineering và temporal leakage | Xây transaction features; history/window features chỉ khi đủ time/entity; audit tính khả dụng; cập nhật baseline | Feature catalog; mã features; leakage audit | Mỗi feature có nguồn, công thức, dtype và thời điểm khả dụng; không đọc tương lai/nhãn; ghi features không thể xây |
| 6 | 23–29/11 | Train XGBoost và so sánh baseline | Train trên features đã kiểm tra; so sánh validation cùng split; ghi cấu hình và tài nguyên | XGBoost checkpoint; experiment log; bảng so sánh | Training tái lập; có metrics hai thuật toán và phân tích chênh lệch; chưa dùng test |
| 7 | 30/11–06/12 | Tuning, imbalance và threshold | Tuning trong ngân sách; class weighting hoặc resampling phù hợp trên train; phân tích precision–recall/FPR validation; chọn threshold | Tuning log; threshold decision record; cấu hình được khóa | Có lý do chọn threshold theo mục tiêu thống nhất; validation giữ phân phối gốc; test không tham gia tuning |
| 8 | 07–13/12 | Final evaluation và error analysis | Đánh giá hai mô hình đã khóa trên test độc lập; phân tích FP/FN và các lát cắt đủ mẫu | Final metrics; confusion matrices; error analysis | Đủ metrics cho hai mô hình, split và threshold rõ ràng; không sửa theo lỗi test rồi báo lại như đánh giá độc lập |
| 9 | 14–20/12 | Artifact và kiểm thử inference | Lưu model, preprocessing, schema, threshold, metadata; load lại; kiểm tra input hợp lệ/sai schema | Artifact bundle; batch inference entry point; kiểm tra reload/input | Predict sau reload nhất quán; output có score, decision và version; lỗi schema được phát hiện |
| 10 | 21–27/12 | Báo cáo và tái lập | Viết báo cáo; chạy lại từ môi trường sạch; chuẩn hóa dependencies, config và repository | Báo cáo dự thảo; reproduction guide; execution log | Có thể chạy từ dữ liệu được cấp quyền đến metrics/artifact; giải thích sai khác môi trường; không tuning bằng test |
| 11 | 28–31/12 | Kiểm tra cuối và hoàn thành v1 | Rà DoD; đối chiếu artifact, báo cáo và logs; hoàn thiện tài liệu | Báo cáo cuối kỳ; bàn giao Model v1; checklist bằng chứng | Đầu ra bắt buộc đầy đủ, nhất quán; blocker được nêu minh bạch; không tuyên bố hoàn thành khi còn thiếu |

## 7. Milestones

| Hạn năm 2026 | Mốc dự kiến | Bằng chứng cần có |
|---|---|---|
| 01/11 | Chốt dataset | Decision record, schema/labels/leakage review và ý kiến giảng viên |
| 15/11 | Logistic Regression baseline hoàn thành | Pipeline, cấu hình và validation metrics tái lập |
| 29/11 | XGBoost được huấn luyện | Checkpoint, log và so sánh validation |
| 13/12 | Hoàn thành đánh giá mô hình | Test metrics độc lập, confusion matrices, threshold và error analysis |
| 31/12 | Hoàn thành Fraud Detection Model v1 | Artifact, batch inference, reproduction guide, báo cáo và DoD |

Nếu chậm mốc, ghi nguyên nhân và điều chỉnh khối lượng tuning/features; bảo toàn hai thuật toán, test độc lập và deliverables bắt buộc.

## 8. Technical Principles

- **Temporal split:** ưu tiên train → validation → test theo thời gian khi phù hợp; ghi cutoff, độ phân giải và cách xử lý timestamp trùng. Nếu không khả thi, ghi lý do, phương án thay thế và hạn chế; cân nhắc entity overlap theo mục tiêu đánh giá.
- **Point-in-time features:** không dùng tương lai. History aggregates chỉ dùng sự kiện trước giao dịch hiện tại; không tạo thứ tự giả cho sự kiện cùng timestamp. Ghi entity key, window và khởi tạo state. Lịch sử từ tập trước chỉ dùng theo quy tắc nhân quả, không dùng nhãn validation/test.
- **Target leakage:** không dùng fraud label hoặc biến tiết lộ trực tiếp nhãn làm input. Loại biến hậu giao dịch/cảnh báo/điều tra chưa chứng minh khả dụng; không mặc định balances của PaySim an toàn.
- **Fit trên train:** preprocessing, feature selection và resampling chỉ fit trên training set; nếu cross-validation, chỉ fit trên training fold. Validation/test chỉ transform bằng pipeline đã fit.
- **Test isolation:** không dùng test để chọn features, hyperparameters, weights, early stopping hoặc threshold. Khóa cấu hình trước final evaluation. Nếu sửa mô hình dựa trên test, cần test độc lập mới để có kết luận mới.
- **Class imbalance:** dùng class weighting hoặc phương pháp phù hợp, tính weights từ train. Resampling chỉ trên train, kiểm tra tính hợp lý với time/category features. Đánh giá validation/test trên phân phối dữ liệu gốc.
- **Metrics:** không chỉ dùng Accuracy. Positive class là fraud; báo Precision, Recall, F1-score, PR-AUC, confusion matrix (TP/FP/TN/FN) và FPR = FP / (FP + TN). Ghi cách tính PR-AUC, phân biệt Average Precision với tích phân hình thang; dùng nhất quán. Nêu cách xử lý metrics không xác định khi thiếu lớp hoặc không có positive predictions.
- **Threshold:** chọn trên validation theo trade-off FP/FN và mục tiêu đã thống nhất, ví dụ tối đa Recall dưới ràng buộc Precision/FPR; không tự đặt mức ràng buộc chưa xác nhận. Lưu threshold, quy tắc score >= threshold và metrics validation trước khi mở test.
- **Feature schema:** mỗi feature có tên, định nghĩa, dtype, đơn vị, nguồn, missing/default policy và thời điểm khả dụng; history features thêm key/window/state. Không tự động dùng raw identifiers làm predictors.
- **Reproducibility:** lưu data version/checksum, split manifest, seed, dependency versions, config, lệnh chạy, code revision và experiment logs. Không commit raw dataset hoặc artifact lớn vào Git; ghi vị trí lưu.
- **Khả năng kế thừa:** cân nhắc cách tái tạo features bằng Flink tương lai ngay khi thiết kế, chỉ ghi yêu cầu và giới hạn trong giai đoạn này.
- **Quyền dữ liệu:** không sử dụng dữ liệu nội bộ ngân hàng khi chưa có quyền và phê duyệt phù hợp; kiểm tra điều kiện truy cập, sử dụng và phân phối trước khi lấy/chia sẻ dữ liệu.

## 9. Deliverables

Các vị trí dưới đây là dự kiến, không khẳng định đầu ra đã tồn tại.

| Đầu ra | Nội dung cần bàn giao | Vị trí dự kiến |
|---|---|---|
| Dataset documentation | Nguồn, phiên bản, quyền sử dụng, schema, labels, thời gian, lựa chọn và hạn chế | docs/ và metadata; không kèm raw dataset |
| EDA và split | Missing values, duplicates, fraud rate, plots, cutoff và quy tắc split | notebooks/01_eda.ipynb; config/; reports/ |
| Preprocessing và features | Pipeline, feature catalog và leakage audit | src/features.py; notebooks/02_preprocessing_pipeline.ipynb; docs/ |
| Training và comparison | Hai thuật toán, configs, seeds, tuning log, validation metrics | src/models.py; notebooks/03_baseline_and_models.ipynb; reports/ |
| Final evaluation | Metrics, PR curves, confusion matrices, threshold, error analysis | src/evaluate.py; reports/; reports/figures/ |
| Artifact bundle | Model, preprocessing, schema, threshold và version metadata | Vị trí lưu được tài liệu hóa; không mặc định commit binary |
| Batch inference | Entry point, input/output contract, schema validation và ví dụ chạy | src/ và hướng dẫn trong docs/ |
| Reproduction và báo cáo | Dependency versions, cách lấy dữ liệu hợp lệ, lệnh training/evaluation/inference, giới hạn | docs/; reports/ |

## 10. Definition of Done

Checklist là điều kiện nghiệm thu trong tương lai, hiện chưa đánh dấu hoàn thành.

- [ ] Dataset được lựa chọn và tài liệu hóa.
- [ ] EDA hoàn thành.
- [ ] Preprocessing pipeline hoạt động.
- [ ] Logistic Regression baseline hoàn thành.
- [ ] XGBoost được huấn luyện.
- [ ] Feature engineering không có leakage đã biết.
- [ ] Đánh giá trên test set độc lập.
- [ ] Có bảng so sánh các metrics.
- [ ] Classification threshold được xác định.
- [ ] Model artifact được lưu.
- [ ] Batch inference chạy được.
- [ ] Có hướng dẫn tái lập kết quả.
- [ ] Báo cáo cuối kỳ hoàn thành.

Mỗi mục khi hoàn tất cần liên kết file, artifact hoặc log làm bằng chứng. Nếu thiếu đầu ra bắt buộc, ghi chưa hoàn thành thay vì suy diễn từ lịch.

## 11. Future Integration Considerations

Chuẩn bị khả năng kế thừa cho HUST kỳ 2027.1, chỉ ở mức hợp đồng dữ liệu và thiết kế:

- **Event schema:** phân biệt transaction ID, account identifiers và event time; ghi đơn vị, timezone nếu có và giới hạn của thời gian tương đối; không tự gán timestamp thực cho step.
- **Feature parity:** tách transaction features và history/state features; lưu công thức, lookback window và quy tắc thiếu lịch sử để đối chiếu batch/streaming sau này.
- **Ordering:** ghi yêu cầu với timestamp trùng, late/out-of-order events, duplicates và state retention; chưa triển khai Flink.
- **Inference contract:** giữ tên/thứ tự/dtype features, preprocessing version, model version, score và threshold.
- **Giới hạn chuyển giao:** synthetic data, biến ẩn danh, thiếu account IDs hoặc khác mục tiêu nhãn cần được đánh giá lại trước áp dụng trên dữ liệu mới.
- **Đánh giá tương lai:** ghi nhu cầu drift monitoring, label delay và chất lượng dữ liệu khi có luồng thật; chưa triển khai monitoring/hạ tầng trong giai đoạn này.

Dataset chính thức cần xác nhận qua cổng quyết định tuần 2 và ý kiến giảng viên. Mục tiêu vận hành và ràng buộc threshold cần thống nhất trước final evaluation. Kế hoạch không giả định AML tương đương transaction fraud và không cam kết kết quả trong môi trường ngân hàng thực tế.
