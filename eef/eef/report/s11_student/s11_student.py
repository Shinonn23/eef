# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters: dict | None = None):
    """Return columns and data for the report.

    This is the main entry point for the report. It accepts the filters as a
    dictionary and should return columns and data. It is called by the framework
    every time the report is refreshed or a filter is updated.
    """

    # print("server", filters)  # You can remove this line after debugging

    fields = [
        # accommodation_section
        "accommodation_condition",
        "accommodation_safety",
        # food_and_dining
        "food_availability",
        "food_cleanliness",
        "food_price_appropriateness",
        # physical_wellbeing
        "medical_facility_access",
        "exercise_facility_access",
        "amenities_access",
        # personal_health_status (*)
        "personal_health_status",
        # stress_or_anxiety
        "academic_stress",
        "adaptation_stress",
        "personal_stress",
        # social_relation
        "college_activity",
        # emotion_management
        "coping_skill",
        # counseling_access
        "mental_health_promo",
        # new_environment_adaptation
        "adapt_academic",
        "adapt_social",
        # time_management
        "time_manage",
        # financial_management
        "expense_manage",
        # debt_level (*)
        "debt_level",
        # monthly_saving (*)
        "monthly_saving",
        # transportation
        "commute_access",
        # access_to_information_and_services
        "service_access",
        # problems_and_obstacles_that_may_occur
        "study_problems",
        "family_problems",
        "relationship_problems",
        "legal_issues",
        "addiction",
        # support_received_and_needed
        "support_family_level",
        "support_peer_level",
        "support_college_access",
        # additional_requirements (#)
        "support_additional_needs",
        "support_suggestions",
    ]

    doc = frappe.get_all("S11 Student", filters=filters, fields=fields)

    columns = get_columns()
    data = get_data(doc)

    # Prepare optional report extras: chart and report_summary
    chart = build_chart(columns, data)
    report_summary = build_report_summary(total=len(doc), data=data)

    # The framework expects (columns, data) by default. We can optionally
    # return chart and report_summary after them. Returning them in this
    # specific order is what the framework expects.
    message = """
    <h5>📊 ระดับคะแนนเปอร์เซ็นต์</h5>
    <ul>
        <li><strong style="color: green;">80-100%</strong> = ระดับดีมาก (สถานการณ์เป็นไปได้ดี)</li>
        <li><strong style="color: blue;">60-79%</strong> = ระดับดี (สถานการณ์ค่อนข้างดี)</li>
        <li><strong style="color: orange;">40-59%</strong> = ระดับปานกลาง (ควรให้ความสนใจ)</li>
        <li><strong style="color: red;">ต่ำกว่า 40%</strong> = ระดับต้องปรับปรุง (ต้องการความช่วยเหลือเร่งด่วน)</li>
    </ul>

    <h5>✅ การแปลความหมาย</h5>
    <p><strong>ข้อมูลทั้งหมดในรายงานนี้แสดงผลเชิงบวก</strong> ค่าเปอร์เซ็นต์ที่สูงขึ้น = สถานการณ์ดีขึ้น</p>
    <ul>
        <li><strong>ความสามารถในการจัดการ:</strong> เช่น การจัดการความเครียด, การรับมือกับปัญหา</li>
        <li><strong>การปลอดจาก:</strong> เช่น ปลอดจากปัญหากฎหมาย, ปลอดจากสิ่งเสพติด</li>
    </ul>
    <p>ตัวอย่าง: "ความสามารถในการจัดการความเครียดจากการเรียน 85%" = นักศึกษาจัดการความเครียดได้ดีมาก ✓</p>

    <h5>📝 ข้อมูลเฉพาะ</h5>
    <ul>
        <li><strong>ระดับปัญหาด้านสุขภาพ:</strong> แสดงค่าเฉลี่ยเป็นข้อความ (สุขภาพไม่ดี / ค่อนข้างดี / ดี / ดีมาก)</li>
        <li><strong>ระดับหนี้สิน:</strong> แสดงค่าเฉลี่ยช่วงหนี้สิน (ไม่มีหนี้ / น้อยกว่า 5000 / 5000-20000 / มากกว่า 20000)</li>
        <li><strong>การออมรายเดือน:</strong> แสดงค่าเฉลี่ยช่วงการออม (0-500 / 500-1000 / 1000-2000 / มากกว่า 2000 บาท)</li>
    </ul>
    """

    return columns, data, message, chart, report_summary


def get_columns() -> list[dict]:
    """Return columns for the report.

    One field definition per column, just like a DocType field definition.
    """
    return [
        # Accommodation Section
        {
            "label": _("ความเหมาะสมของสภาพที่พักอาศัย"),
            "fieldname": "accommodation_condition",
            "fieldtype": "Percent",
            "width": 150,
        },
        {
            "label": _("ความปลอดภัยของที่พัก"),
            "fieldname": "accommodation_safety",
            "fieldtype": "Percent",
            "width": 150,
        },
        # Food and Dining
        {
            "label": _("ความเพียงพอของร้านอาหาร"),
            "fieldname": "food_availability",
            "fieldtype": "Percent",
            "width": 150,
        },
        {
            "label": _("ความสะอาดและสุขอนามัย"),
            "fieldname": "food_cleanliness",
            "fieldtype": "Percent",
            "width": 150,
        },
        {
            "label": _("ความเหมาะสมของราคา"),
            "fieldname": "food_price_appropriateness",
            "fieldtype": "Percent",
            "width": 150,
        },
        # Physical Wellbeing
        {
            "label": _("ความเหมาะสมของสถานพยาบาล"),
            "fieldname": "medical_facility_access",
            "fieldtype": "Percent",
            "width": 150,
        },
        {
            "label": _("ความเหมาะสมของแหล่งออกกำลังกาย"),
            "fieldname": "exercise_facility_access",
            "fieldtype": "Percent",
            "width": 150,
        },
        {
            "label": _("ความเหมาะสมของสถานอำนวยความสะดวก"),
            "fieldname": "amenities_access",
            "fieldtype": "Percent",
            "width": 180,
        },
        # Personal Health Status
        {
            "label": _("ระดับปัญหาด้านสุขภาพของตนเอง"),
            "fieldname": "personal_health_status",
            "fieldtype": "Data",
            "width": 150,
        },
        # Stress or Anxiety
        {
            "label": _("ความสามารถในการจัดการความเครียดจากการเรียน"),
            "fieldname": "academic_stress",
            "fieldtype": "Percent",
            "width": 200,
        },
        {
            "label": _("ความสามารถในการจัดการความเครียดจากการปรับตัว"),
            "fieldname": "adaptation_stress",
            "fieldtype": "Percent",
            "width": 200,
        },
        {
            "label": _("ความสามารถในการจัดการความเครียดจากปัญหาส่วนตัว"),
            "fieldname": "personal_stress",
            "fieldtype": "Percent",
            "width": 220,
        },
        # Social Relation
        {
            "label": _("ระดับการมีส่วนร่วมในกิจกรรมของวิทยาลัย"),
            "fieldname": "college_activity",
            "fieldtype": "Percent",
            "width": 180,
        },
        # Emotion Management
        {
            "label": _("ความสามารถในการรับมือกับปัญหาและความผิดหวัง"),
            "fieldname": "coping_skill",
            "fieldtype": "Percent",
            "width": 200,
        },
        # Counseling Access
        {
            "label": _("การประชาสัมพันธ์ถึงการช่วยเหลือด้านสุขภาพจิต"),
            "fieldname": "mental_health_promo",
            "fieldtype": "Percent",
            "width": 200,
        },
        # New Environment Adaptation
        {
            "label": _("ความสามารถในการปรับตัวด้านการเรียน"),
            "fieldname": "adapt_academic",
            "fieldtype": "Percent",
            "width": 180,
        },
        {
            "label": _("ความสามารถในการปรับตัวด้านสังคม"),
            "fieldname": "adapt_social",
            "fieldtype": "Percent",
            "width": 180,
        },
        # Time Management
        {
            "label": _("ความสามารถในการบริหารเวลา"),
            "fieldname": "time_manage",
            "fieldtype": "Percent",
            "width": 150,
        },
        # Financial Management
        {
            "label": _("ความสามารถในการบริหารจัดการค่าใช้จ่าย"),
            "fieldname": "expense_manage",
            "fieldtype": "Percent",
            "width": 180,
        },
        {
            "label": _("ระดับปัญหาหนี้สินส่วนตัว"),
            "fieldname": "debt_level",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("ความสามารถในการออมต่อเดือน"),
            "fieldname": "monthly_saving",
            "fieldtype": "Data",
            "width": 150,
        },
        # Transportation
        {
            "label": _("ความสะดวกในการเดินทาง"),
            "fieldname": "commute_access",
            "fieldtype": "Percent",
            "width": 150,
        },
        # Access to Information and Services
        {
            "label": _("ระดับการรับรู้ถึงข้อมูลและบริการสำคัญ"),
            "fieldname": "service_access",
            "fieldtype": "Percent",
            "width": 180,
        },
        # Problems and Obstacles
        {
            "label": _("ความสามารถในการรับมือกับปัญหาด้านการเรียน"),
            "fieldname": "study_problems",
            "fieldtype": "Percent",
            "width": 200,
        },
        {
            "label": _("ความสามารถในการรับมือกับปัญหาครอบครัว"),
            "fieldname": "family_problems",
            "fieldtype": "Percent",
            "width": 200,
        },
        {
            "label": _("ความสามารถในการรับมือกับปัญหาความสัมพันธ์"),
            "fieldname": "relationship_problems",
            "fieldtype": "Percent",
            "width": 220,
        },
        {
            "label": _("การปลอดจากปัญหาทางกฎหมาย/ความปลอดภัย"),
            "fieldname": "legal_issues",
            "fieldtype": "Percent",
            "width": 220,
        },
        {
            "label": _("การปลอดจากสิ่งเสพติดและพฤติกรรมเสี่ยง"),
            "fieldname": "addiction",
            "fieldtype": "Percent",
            "width": 220,
        },
        # Support Received and Needed
        {
            "label": _("ระดับการสนับสนุนจากครอบครัว"),
            "fieldname": "support_family_level",
            "fieldtype": "Percent",
            "width": 150,
        },
        {
            "label": _("การมีกลุ่มเพื่อนที่คอยช่วยเหลือ"),
            "fieldname": "support_peer_level",
            "fieldtype": "Percent",
            "width": 150,
        },
        {
            "label": _("การเข้าถึงบริการของวิทยาลัย"),
            "fieldname": "support_college_access",
            "fieldtype": "Percent",
            "width": 150,
        },
        # Additional Requirements
        {
            "label": _("สิ่งที่นักศึกษาต้องการความช่วยเหลือเพิ่มเติม"),
            "fieldname": "support_additional_needs",
            "fieldtype": "Long Text",
            "width": 400,
        },
        {
            "label": _("ข้อเสนอแนะอื่นๆ"),
            "fieldname": "support_suggestions",
            "fieldtype": "Long Text",
            "width": 400,
        },
    ]


def get_data(doc_list: list[dict]) -> list[list]:
    """Return data for the report.
    The report data is a list of rows, with each row being a list of cell values.
    """
    if not doc_list:
        return []

    health_status_map = {
        "สุขภาพไม่ดี": 1,
        "สุขภาพค่อนข้างดี": 2,
        "สุขภาพดี": 3,
        "สุขภาพดีมาก": 4,
    }

    debt_level_map = {
        "ไม่มีหนี้": 1,
        "น้อยกว่า 5000 บาท": 2,
        "5000-20000 บาท": 3,
        "มากกว่า 20000 บาท": 4,
        "ไม่ระบุ": 0,
    }

    monthly_saving_map = {
        "0-500 บาท": 1,
        "500-1000 บาท": 2,
        "1000-2000 บาท": 3,
        "มากกว่า 2000 บาท": 4,
    }

    health_status_reverse = {v: k for k, v in health_status_map.items()}
    debt_level_reverse = {v: k for k, v in debt_level_map.items()}
    monthly_saving_reverse = {v: k for k, v in monthly_saving_map.items()}

    field_sums = {}
    field_counts = {}

    fields = [
        "accommodation_condition",
        "accommodation_safety",
        "food_availability",
        "food_cleanliness",
        "food_price_appropriateness",
        "medical_facility_access",
        "exercise_facility_access",
        "amenities_access",
        "personal_health_status",
        "academic_stress",
        "adaptation_stress",
        "personal_stress",
        "college_activity",
        "coping_skill",
        "mental_health_promo",
        "adapt_academic",
        "adapt_social",
        "time_manage",
        "expense_manage",
        "debt_level",
        "monthly_saving",
        "commute_access",
        "service_access",
        "study_problems",
        "family_problems",
        "relationship_problems",
        "legal_issues",
        "addiction",
        "support_family_level",
        "support_peer_level",
        "support_college_access",
        "support_additional_needs",
        "support_suggestions",
    ]
    for doc in doc_list:
        for field in fields:
            value = doc.get(field)

            if value is None or value == "":
                continue

            if field in ["support_additional_needs", "support_suggestions"]:
                if field not in field_sums:
                    field_sums[field] = []
                field_sums[field].append(value)
                continue

            numeric_value = None
            if field == "personal_health_status":
                numeric_value = health_status_map.get(value)
            elif field == "debt_level":
                numeric_value = debt_level_map.get(value)
            elif field == "monthly_saving":
                numeric_value = monthly_saving_map.get(value)
            else:
                try:
                    numeric_value = float(value)
                except (ValueError, TypeError):
                    continue

            if numeric_value is not None and (field != "debt_level" or numeric_value > 0):
                if field not in field_sums:
                    field_sums[field] = 0
                    field_counts[field] = 0
                field_sums[field] += numeric_value
                field_counts[field] += 1

    result_row = []

    for field in fields:
        if field in ["support_additional_needs", "support_suggestions"]:
            texts = field_sums.get(field, [])
            if texts:
                formatted_texts = [f"{i + 1}. {text}" for i, text in enumerate(texts)]
                result_row.append("\n\n".join(formatted_texts))
            else:
                result_row.append("")
        elif field in field_counts and field_counts[field] > 0:
            avg = field_sums[field] / field_counts[field]

            if field == "personal_health_status":
                rounded = round(avg)
                result_row.append(health_status_reverse.get(rounded, ""))
            elif field == "debt_level":
                rounded = round(avg)
                result_row.append(debt_level_reverse.get(rounded, ""))
            elif field == "monthly_saving":
                rounded = round(avg)
                result_row.append(monthly_saving_reverse.get(rounded, ""))
            else:
                # For rating fields, multiply by 100 to get percentage
                # For negative indicators (problems/stress), invert the scale
                # so that lower values (less problems) become higher percentages (better)
                negative_indicators = [
                    "academic_stress",
                    "adaptation_stress",
                    "personal_stress",
                    "study_problems",
                    "family_problems",
                    "relationship_problems",
                    "legal_issues",
                    "addiction",
                ]

                if field in negative_indicators:
                    # Invert: 1.0 (high problem) becomes 0%, 0.0 (no problem) becomes 100%
                    # Rating values are in range 0-1, not 0-5
                    percentage = (1 - avg) * 100
                else:
                    # Normal: higher rating = higher percentage
                    # Rating values are in range 0-1, not 0-5
                    percentage = avg * 100

                result_row.append(round(percentage, 2))
        else:
            # No data for this field
            result_row.append(None)

    return [result_row]


def build_chart(columns: list[dict], data: list[list]) -> dict | None:
    """Build a simple bar chart configuration from the report data.

    Shows average values for rating fields in a horizontal bar chart.
    """
    if not data or not data[0]:
        return None

    row = data[0]

    labels = []
    values = []

    for i, col in enumerate(columns):
        if col.get("fieldtype") == "Percent" and i < len(row):
            value = row[i]
            if value is not None and isinstance(value, (int, float)):
                labels.append(col.get("label", col.get("fieldname")))
                values.append(value)

    if not values:
        return None

    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "ค่าเฉลี่ย",
                    "values": values,
                    "chartType": "bar",
                }
            ],
        },
        "type": "bar",
        "height": 400,
        "colors": ["#3b82f6"],
    }

    return chart


def build_report_summary(total: int, data: list[list] | None = None) -> list[dict]:
    """Compute simple aggregates and return report_summary expected by Frappe.

    Show summary statistics grouped by major categories.
    """
    summary = [
        {
            "value": total,
            "label": _("จำนวนแบบสำรวจทั้งหมด"),
            "datatype": "Int",
        }
    ]

    if not data or not data[0]:
        return summary

    row = data[0]

    field_groups = {
        "living_conditions": {
            "label": _("สภาพความเป็นอยู่ทั่วไป"),
            "fields": [
                "accommodation_condition",
                "accommodation_safety",
                "food_availability",
                "food_cleanliness",
                "food_price_appropriateness",
                "medical_facility_access",
                "exercise_facility_access",
                "amenities_access",
            ],
        },
        "mental_health": {
            "label": _("สุขภาพจิตและอารมณ์"),
            "fields": [
                "academic_stress",
                "adaptation_stress",
                "personal_stress",
                "college_activity",
                "coping_skill",
                "mental_health_promo",
            ],
        },
        "college_adaptation": {
            "label": _("การปรับตัวและการใช้ชีวิตในวิทยาลัย"),
            "fields": [
                "adapt_academic",
                "adapt_social",
                "time_manage",
                "expense_manage",
                "commute_access",
                "service_access",
            ],
        },
        "problems": {
            "label": _("ปัญหาและอุปสรรค"),
            "fields": [
                "study_problems",
                "family_problems",
                "relationship_problems",
                "legal_issues",
                "addiction",
            ],
        },
        "support": {
            "label": _("การสนับสนุนที่ได้รับ"),
            "fields": ["support_family_level", "support_peer_level", "support_college_access"],
        },
    }

    all_fields = [
        "accommodation_condition",
        "accommodation_safety",
        "food_availability",
        "food_cleanliness",
        "food_price_appropriateness",
        "medical_facility_access",
        "exercise_facility_access",
        "amenities_access",
        "personal_health_status",
        "academic_stress",
        "adaptation_stress",
        "personal_stress",
        "college_activity",
        "coping_skill",
        "mental_health_promo",
        "adapt_academic",
        "adapt_social",
        "time_manage",
        "expense_manage",
        "debt_level",
        "monthly_saving",
        "commute_access",
        "service_access",
        "study_problems",
        "family_problems",
        "relationship_problems",
        "legal_issues",
        "addiction",
        "support_family_level",
        "support_peer_level",
        "support_college_access",
        "support_additional_needs",
        "support_suggestions",
    ]

    for _group_key, group_info in field_groups.items():
        values = []
        for field in group_info["fields"]:
            if field in all_fields:
                idx = all_fields.index(field)
                if idx < len(row) and row[idx] is not None:
                    value = row[idx]
                    if isinstance(value, (int, float)):
                        values.append(value)

        if values:
            avg = sum(values) / len(values)

            # Determine indicator color
            if avg >= 80:
                indicator = "green"
            elif avg >= 60:
                indicator = "blue"
            elif avg >= 40:
                indicator = "orange"
            else:
                indicator = "red"

            summary.append(
                {
                    "value": round(avg, 1),
                    "indicator": indicator,
                    "label": group_info["label"],
                    "datatype": "Percent",
                }
            )

    all_numeric_values = []
    for value in row:
        if value is not None and isinstance(value, (int, float)):
            all_numeric_values.append(value)

    if all_numeric_values:
        overall_avg = sum(all_numeric_values) / len(all_numeric_values)

        if overall_avg >= 80:
            overall_indicator = "green"
        elif overall_avg >= 60:
            overall_indicator = "blue"
        elif overall_avg >= 40:
            overall_indicator = "orange"
        else:
            overall_indicator = "red"

        summary.append(
            {
                "value": round(overall_avg, 1),
                "indicator": overall_indicator,
                "label": _("ภาพรวมทั้งหมด (Overall)"),
                "datatype": "Percent",
            }
        )

    return summary
