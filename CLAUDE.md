# CLAUDE.md — PKT-Train

โมดูล **PKT Train** ของ PK Transport (PKT = Pongsakorn Klaywun Transportation): สคริปต์เทรนโมเดลตรวจจับวัตถุ (รถ/คน)
ผู้ใช้เป็นคนไทย ไม่ชำนาญ git — **ตอบและอธิบายเป็นภาษาไทย**

## โครงสร้าง

- **git repo:** repo อิสระ https://github.com/boss8152060-cyber/PKT-Train (branch `main`) — **โมดูลของ PK Transport** (ดูหัวข้อ "โมดูลของ PK Transport" ด้านล่าง); แอปหลักติดตั้งไว้ใน `modules/train/`
- สคริปต์ 3 ตัว (แต่ละตัวเขียนเป็น Cell `# %% [Cell N]` ใช้บน Google Colab และรันทั้งไฟล์ในเครื่องได้ — ตรวจเองอัตโนมัติ `RUN_ENV`):
  `Train YOLO26L Augmentation.py`, `Train RTDETR-L Augmentation.py`, `Train RT-DETRv2 PyTorch Augmentation.py` (ดู `README.md`)
- หน้า PKT Train (`pkt_train/page.py`) อ่านและแพตช์ข้อความของสคริปต์เหล่านี้ด้วย regex (`epochs = ...`, `imgsz`, `batch`, `workers`, `patience`, `training_mode`, `source_run_name`, `MODEL_SIZE` และทุกบรรทัด `# @param`):
  **ถ้าเปลี่ยนรูปแบบบรรทัดเหล่านี้ ต้องแก้ `pkt_train/core.py` ใน repo นี้ด้วย** (`tests/test_core.py` `RealScripts` ตรวจให้)
- โฟลเดอร์ที่ไม่ขึ้น git (ดู `.gitignore`): `Runs/`, `_workspace/`, `_original_colab_versions/`, ไฟล์น้ำหนัก (`.pt`, `.pth`, `.engine`)


## โมดูลของ PK Transport (ปลั๊กอิน)

repo นี้เป็น **โมดูลที่ติดตั้งแยก** ใน **PK Transport** (https://github.com/boss8152060-cyber/PK-Transport): แอปหลักโหลดเวอร์ชันที่เลือก (ตาม git tag) จาก GitHub มาไว้ใน `modules/train/` ของแอป ไฟล์ที่เกี่ยวข้อง:

| ไฟล์ | หน้าที่ |
|---|---|
| `pkt_module.json` | บอกแอปหลักว่าโมดูลคืออะไร: `id`, `version`, `min_shell` (PK Transport รุ่นต่ำสุดที่ใช้ได้), ไลบรารีที่ต้องลง (`requirements.txt`), `needs_torch` |
| `pkt_plugin.py` | วิธีที่โมดูลปรากฏในหน้าต่างของแอปหลัก (API เวอร์ชัน 1: `create`, `summary`, `recent`, `texts`, `catalogs`) — **ส่วนบนสุดของไฟล์ต้องเบา** (ห้าม import torch/ไลบรารีหนัก ที่ระดับบน) |
| `pkt_train/` | โค้ดของโมดูล: `page.py` (หน้าเทรน), `core.py` (อ่าน/แพตช์สคริปต์ ไม่ผูก GUI), `runs.py` (หา run ที่เทรนแล้ว), `texts.py` (ข้อความไทย/อังกฤษของหน้า) |

**กฎการปล่อยเวอร์ชัน:** (1) แก้ `version` ใน `pkt_module.json` ให้ตรงกับเลขใน CHANGELOG (มีเทสต์ตรวจ) (2) commit ชื่อ `PKT-Train x.y.z: <คำอธิบาย_แบบ_CamelCase>` (3) ติด tag `v<x.y.z>` แล้ว push พร้อม tag — แอปหลักเห็นเวอร์ชันใหม่จาก tag และให้ผู้ใช้อัปเดต/ย้อนเวอร์ชันได้ (4) ถ้าเปลี่ยนวิธีที่ใช้ API ของแอปหลัก ให้ปรับ `min_shell`
**ข้อมูลของผู้ใช้ห้ามเขียนในโฟลเดอร์ของโมดูล** (โฟลเดอร์นี้ถูกแทนที่ทั้งก้อนเมื่ออัปเดต/ย้อนเวอร์ชัน): ใช้โฟลเดอร์จากตัวแปร `PKT_USER_DATA` (แอปหลักตั้งให้) หรือ `app.user_data_dir(...)`
ทดสอบกับแอปหลัก: ตั้งโฟลเดอร์นี้เป็น "โฟลเดอร์ที่เชื่อมไว้" ในหน้าตั้งค่าของ PK Transport (หรือรัน `tests/gui_real_modules.py` / `gui_train_module.py` ใน PK-Transport ด้วย `PKT_MODULES_SRC`)

## กฎของสคริปต์

- **ห้ามทำให้ Colab พัง:** พฤติกรรมบน Colab ต้องเหมือนเดิม (path ของ Drive, `# @param`, การคัดลอกทีละ Cell); ส่วนที่มีผลข้างเคียงต้องอยู่ใต้ `if IS_MAIN:` (Windows ตัวโหลดข้อมูลแบบหลายโปรเซสนำไฟล์ไปอ่านใหม่)
- ไม่มีคำสั่งแบบ notebook (`!pip`, `!ls`) ในไฟล์ — ใช้ `subprocess` แทน เพื่อให้รันเป็นไฟล์ `.py` ได้
- ก่อน commit: ตรวจ syntax ทุกไฟล์ (`python -c "import ast,sys;ast.parse(open(sys.argv[1],encoding='utf-8').read())" <ไฟล์>`); ถ้าแก้ตรรกะเทรน ให้ทดสอบจริงด้วยชุดข้อมูลจิ๋ว/โมเดลจาก yaml (ไม่ต้องดาวน์โหลดน้ำหนัก) ตามที่ทำใน 0.2.0 — RT-DETRv2 ยังไม่เคยทดสอบรันจริง

## กฎการใช้ git

หลังทำงานเสร็จและตรวจแล้ว commit + push ให้เอง (remote `origin` ของ repo นี้เท่านั้น):

```
PKT-Train <x.y.z>: <คำอธิบายสั้น ๆ_แบบ_CamelCase> [(PASS)]
```

- **ชื่อ repo นำหน้าเลขเวอร์ชัน เหมือนกันทุก repo ของ PK Transport** (`PK-Transport` / `PKT-Analyze` / `PKT-Data` / `PKT-Train`); commit เก่าไม่แก้
- `y` ขึ้นเมื่อมีความสามารถใหม่ (เช่นรองรับรุ่น/โมเดลใหม่), `z` เมื่อแก้/ปรับเรื่องเดิมหรือเอกสาร
- ทุก commit: เพิ่มบรรทัดใน `CHANGELOG.md` + ติด tag `v<x.y.z>` + `git push` พร้อม `git push origin v<x.y.z>`
- `(PASS)` เฉพาะเมื่อผู้ใช้ยืนยันแล้วว่าผ่าน; บรรทัดสุดท้ายของ message ใส่ trailer `Co-Authored-By: ...` ตามที่ระบบกำหนด
- **ห้าม** `git push --force`, `git reset --hard`, `git rebase`, `git commit --amend` กับ commit ที่ push แล้ว, ลบ branch/tag/ประวัติ โดยไม่ขออนุญาต; ห้าม push ไป remote อื่น
