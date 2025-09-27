# Branch Naming Convention

เพื่อให้การพัฒนาโค้ดเป็นระเบียบ เข้าใจง่าย และสามารถทำงานร่วมกันได้อย่างมีประสิทธิภาพ
โปรเจกต์นี้ใช้หลักการตั้งชื่อ branch ตามหมวดหมู่ดังนี้:

## หลักการตั้งชื่อ

- ใช้รูปแบบ:

    ```
    <type>/<short-description>
    ```

- `type` = ประเภทของการเปลี่ยนแปลง

- `short-description` = คำอธิบายสั้น ๆ (ภาษาอังกฤษสั้น กระชับ, คั่นด้วย `-`)

ตัวอย่าง:

```
feature/add-user-login
fix/resolve-auth-bug
refactor/improve-db-layer
```

---

## ประเภทของ Branch

### `feature/`

- ใช้เมื่อ: เพิ่มฟีเจอร์ใหม่ หรือเพิ่มความสามารถใหม่เข้าระบบ
- ตัวอย่าง:
    - `feature/add-dashboard`
    - `feature/payment-integration`

### `fix/` หรือ `bugfix/`

- ใช้เมื่อ: แก้ไขบั๊กทั่วไปที่พบ
- ตัวอย่าง:
    - `fix/login-error`
    - `bugfix/email-sending`

### `refactor/`

- ใช้เมื่อ: ปรับปรุงโครงสร้างโค้ด, เพิ่มคุณภาพโค้ด แต่ไม่เพิ่มฟีเจอร์ และไม่แก้บั๊กโดยตรง
- ตัวอย่าง:
    - `refactor/cleanup-controllers`
    - `refactor/optimize-query`

### `chore/`

- ใช้เมื่อ: งานเบ็ดเตล็ด เช่น อัปเดต dependency, ปรับ CI/CD, config, tooling
- ตัวอย่าง:
    - `chore/update-dependencies`
    - `chore/setup-prettier`

### `hotfix/`

- ใช้เมื่อ: แก้บั๊กด่วนใน production ที่ต้องแก้ทันที
- ตัวอย่าง:
    - `hotfix/fix-critical-crash`
    - `hotfix/patch-security-issue`

### `docs/`

- ใช้เมื่อ: แก้ไขหรือเพิ่มเอกสาร เช่น README, Wiki, API docs
- ตัวอย่าง:
    - `docs/update-readme`
    - `docs/add-api-guide`

---

## สรุป

การตั้งชื่อ branch ให้ชัดเจน จะช่วยให้ทีม:

- เข้าใจ scope ของงานได้ทันที
- จัดการ PR/MR ได้ง่าย
- ลดความสับสนในการ merge
