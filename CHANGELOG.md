# CHANGELOG — PKT-Train

เลขเวอร์ชัน `x.y.z` (tag `vx.y.z`): `y` = ความสามารถใหม่, `z` = แก้/ปรับเรื่องเดิมหรือเอกสาร

| เวอร์ชัน | commit | ชื่อ | ทำอะไร |
|---|---|---|---|
| **0.1.0** | `300235f` | PKT-Train 0.1.0: Import_Original_Colab_Training_Scripts | สคริปต์เทรนเดิมที่ใช้บน Google Colab (YOLO26, RT-DETR-L, RT-DETRv2) |
| **0.2.0** | `8359888` | PKT-Train 0.2.0: Local_Training_Mode_And_Model_Size_Selection | รันได้ทั้ง Colab และในเครื่อง, เลือกรุ่นโมเดล (YOLO26 n/s/m/l/x, RT-DETR l/x, RT-DETRv2 s/m*/m/l/x), รองรับ Windows, README |
| **0.2.1** | `890538d` | PKT-Train 0.2.1: Docs_CommitMessageFormat_ClaudeMd_Changelog | เพิ่ม `CLAUDE.md` (กฎของ repo + รูปแบบ commit `PKT-Train x.y.z: ...`) และ `CHANGELOG.md` (ชื่อ commit สองรายการแรกเป็นรูปแบบเดิมก่อนปรับชื่อ) |
| **0.3.0** | (commit นี้) | PKT-Train 0.3.0: PKTrainModuleWithTrainingPage | PKT Train เป็นโมดูลของ PK Transport: หน้าเทรน (เดิมเป็นโค้ดของแอปหลัก) ย้ายมาอยู่ใน repo นี้ (`pkt_train/page.py`, `core.py`, `runs.py`, `texts.py`) พร้อม `pkt_module.json` / `pkt_plugin.py`; ผลเทรนและสำเนาสคริปต์ที่แพตช์เก็บใน `user_data/PKT-Train/` ของแอปหลัก (นอกโฟลเดอร์โมดูล ไม่หายเมื่ออัปเดต/ถอน); สคริปต์เทรน 3 ตัวไม่เปลี่ยน; เทสต์ย้ายมาด้วย (`tests/test_core.py`, `test_runs.py`) |

เวอร์ชันถัดไป: งานต่อเรื่องเดิม = `0.2.2`; ความสามารถใหม่ = `0.3.0`
