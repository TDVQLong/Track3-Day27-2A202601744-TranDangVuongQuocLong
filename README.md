# Bài Lab 2T: Xây dựng Workflow kiểm duyệt bằng LangGraph và Streamlit

Đây là bài lab kết hợp sức mạnh của LangGraph để tạo ra một biểu đồ trạng thái (StateGraph) quản lý quy trình hành động (Action Flow) kết hợp với **Streamlit** để thực hiện sự tương tác của con người (Human-in-the-loop).

## Cài đặt (Dependencies)

Để chạy dự án này, bạn cần cài đặt các thư viện được liệt kê trong `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Cách chạy ứng dụng

1. Di chuyển vào thư mục dự án.
2. Chạy file `app.py` bằng Streamlit:

```bash
streamlit run app.py
```

## Luồng hoạt động (Workflow & Hard rules)

Hệ thống đánh giá khách hàng (ví dụ: cấp tín dụng hoặc gửi email khuyến mãi).
Có ba luật chính được thiết lập:

- **Policy Override (Ghi đè chính sách)**: Nếu hành động là `increase_credit_limit` (tăng hạn mức tín dụng), mức độ rủi ro rất cao nên hệ thống LUÔN LUÔN yêu cầu người dùng xác nhận, bất kể Confidence Score là bao nhiêu.
- **Auto-Execute (Tự động thực thi)**: Nếu hành động rủi ro thấp (như `send_email`) VÀ mức độ tự tin (Confidence score) `>= 0.85`, hệ thống sẽ tự động thực thi.
- **Escalate/Suggest (Chuyển tiếp/Đề xuất duyệt)**: Nếu Confidence score `< 0.85`, hệ thống sẽ luôn cần người duyệt (dù cho đó là rủi ro thấp).

## Hướng dẫn thao tác trên Streamlit

1. Nhập thông tin yêu cầu ở Sidebar (bên trái).
2. Nhấn **Submit Request**.
3. Nếu yêu cầu vi phạm `Hard Policy` hoặc Confidence score dưới `0.85`, đồ thị LangGraph sẽ bị dừng lại bằng cơ chế `interrupt_before`.
4. Trên giao diện chờ duyệt, bạn có thể nhấn:
   - **Approve**: Phê duyệt yêu cầu.
   - **Reject**: Từ chối yêu cầu.
   - **Edit Action**: Sửa đổi hành động đề xuất.
5. Sau khi lựa chọn, đồ thị tiếp tục chạy đến bước lưu vào file Audit log.

## Vị trí Audit Log

Mọi quyết định (Auto-Execute hoặc Human Decision) đều được ghi lại.
File Audit log được lưu ở: `audit_log.json` (nằm ở thư mục gốc của dự án).