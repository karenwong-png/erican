# -*- coding: utf-8 -*-
"""Map popup bodies. These only enter the DOM when a marker is clicked, so the
rendered-page sweep never sees them; they are taken from PLACES[].desc in the
source instead, plus the two fixed fragments the popup template adds."""
import io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
keys = json.load(io.open(os.path.join(HERE, 'popups.json'), encoding='utf-8'))
T = [
("校园 —— Block C, First Floor, Megan Avenue II, No. 12 Jalan Yap Kwan Seng，距双子塔仅数分钟步行路程。", "Kampus — Block C, First Floor, Megan Avenue II, No. 12 Jalan Yap Kwan Seng, beberapa minit berjalan dari Menara Berkembar Petronas.", "الحرم — Block C, First Floor, Megan Avenue II, No. 12 Jalan Yap Kwan Seng، على بعد دقائق سيرًا من برجي بتروناس."),
("555 Jalan Cheras, Taman Pertama —— 五座塔楼，3,684 个单位，Taman Pertama MRT 就在门口。", "555 Jalan Cheras, Taman Pertama — lima menara, 3,684 unit, Taman Pertama MRT di depan pintu.", "555 Jalan Cheras, Taman Pertama — خمسة أبراج، ٣٬٦٨٤ وحدة، ومحطة Taman Pertama عند الباب."),
("Jalan Cheras, Taman Pertama —— 一栋 41 层大楼，507 个单位，2025 年落成，步行可达两个地铁站。", "Jalan Cheras, Taman Pertama — satu menara 41 tingkat, 507 unit, siap 2025, dua stesen MRT dalam jarak berjalan.", "Jalan Cheras, Taman Pertama — برج من ٤١ طابقًا، ٥٠٧ وحدات، اكتمل عام ٢٠٢٥، ومحطتا مترو على مسافة المشي."),
("Jalan Pudu Impian, Cheras —— 39 层，795 个单位，四大区域四十余项设施。", "Jalan Pudu Impian, Cheras — 39 tingkat, 795 unit, 40+ kemudahan dalam empat zon.", "Jalan Pudu Impian, Cheras — ٣٩ طابقًا، ٧٩٥ وحدة، وأكثر من ٤٠ مرفقًا في أربع مناطق."),
("Jalan Atmosphere Utama 2, Pusat Bandar Putra Permai, Seri Kembangan —— 1,452 户，坐落于生活商场之上，距 Taman Putra Permai MRT 200 米，与校园同属一条线。", "Jalan Atmosphere Utama 2, Pusat Bandar Putra Permai, Seri Kembangan — 1,452 kediaman di atas pusat beli-belah gaya hidup, 200 m ke Taman Putra Permai MRT pada laluan yang sama dengan kampus.", "Jalan Atmosphere Utama 2, Pusat Bandar Putra Permai, Seri Kembangan — ١٬٤٥٢ وحدة فوق مركز تسوق، و٢٠٠ م إلى محطة Taman Putra Permai على خط الحرم نفسه."),
("主校园，1016 Jalan Sultan Ismail —— 距 Erican College 最近的另一所院校。", "Kampus utama, 1016 Jalan Sultan Ismail — kampus lain yang terdekat dengan Erican College.", "الحرم الرئيسي، 1016 Jalan Sultan Ismail — أقرب حرم جامعي آخر إلى Erican College."),
("马来西亚历史最悠久的公立研究型大学 —— Lembah Pantai。", "Universiti penyelidikan awam tertua Malaysia — Lembah Pantai.", "أقدم جامعة بحثية حكومية في ماليزيا — Lembah Pantai."),
("拉曼管理与科技大学，Jalan Genting Klang。", "Universiti Tunku Abdul Rahman Pengurusan & Teknologi, Jalan Genting Klang.", "جامعة Tunku Abdul Rahman للإدارة والتكنولوجيا، Jalan Genting Klang."),
("马来西亚国际伊斯兰大学主校园。", "Kampus utama Universiti Islam Antarabangsa Malaysia.", "الحرم الرئيسي للجامعة الإسلامية العالمية بماليزيا."),
("位于 Jalan Kia Peng 的私立医院 —— 距校园最近。", "Hospital swasta di Jalan Kia Peng — paling dekat dengan kampus.", "مستشفى خاص في Jalan Kia Peng — الأقرب إلى الحرم."),
("马来西亚最大的政府医院 —— Jalan Pahang。", "Hospital kerajaan terbesar Malaysia — Jalan Pahang.", "أكبر مستشفى حكومي في ماليزيا — Jalan Pahang."),
("位于 Jalan Peel, Cheras 的私立医院 —— 距 Cheras 各住宅最近。", "Hospital swasta di Jalan Peel, Cheras — terdekat dengan kediaman di Cheras.", "مستشفى خاص في Jalan Peel, Cheras — الأقرب إلى مساكن Cheras."),
("私立专科医院 —— Jalan Mamanda 9, Ampang。", "Hospital pakar swasta — Jalan Mamanda 9, Ampang.", "مستشفى تخصصي خاص — Jalan Mamanda 9, Ampang."),
("156 Jalan Ampang，双子塔对面 —— 距校园最近的商场。", "156 Jalan Ampang, bertentangan Menara Berkembar — pusat beli-belah terdekat dengan kampus.", "156 Jalan Ampang، مقابل البرجين التوأمين — أقرب مركز تسوق إلى الحرم."),
("Jalan Tun Razak，Jalan Ampang 交汇处 —— 杂货与美食广场。", "Jalan Tun Razak, di persimpangan Jalan Ampang — barangan runcit dan medan selera.", "Jalan Tun Razak، عند تقاطع Jalan Ampang — بقالة وساحات طعام."),
("Jalan Peel, Cheras —— 服务 Taman Pertama 与 Pudu Impian 各住宅的大型商场。", "Jalan Peel, Cheras — pusat beli-belah besar untuk kediaman Taman Pertama dan Pudu Impian.", "Jalan Peel, Cheras — المركز التجاري الكبير لمساكن Taman Pertama وPudu Impian."),
("Jalan Cochrane，紧邻 Maluri MRT–LRT 转乘站。", "Jalan Cochrane, bersebelahan pertukaran MRT–LRT Maluri.", "Jalan Cochrane، بجوار تقاطع Maluri لـ MRT–LRT."),
("双峰塔 —— 办公楼、商场与城市地标，距校园步行可达。", "Menara Berkembar Petronas — pejabat, pusat beli-belah dan mercu tanda bandar, berdekatan kampus.", "برجا بتروناس التوأمان — مكاتب ومركز تسوق ومعلم المدينة، على مسافة قصيرة من الحرم."),
("吉隆坡的国际金融区，也是 Cheras 各住宅的换乘点。", "Daerah kewangan antarabangsa Kuala Lumpur, dan titik pertukaran bagi kediaman di Cheras.", "الحي المالي الدولي في كوالالمبور، ونقطة التبديل لمساكن Cheras."),
("交通枢纽与办公中心 —— Brickfields。", "Hab pengangkutan dan pejabat — Brickfields.", "مركز نقل ومكاتب — Brickfields."),
]
assert len(T) == len(keys), '%d translations for %d keys' % (len(T), len(keys))
out = {k: list(v) for k, v in zip(keys, T)}
out["from Erican College"] = ["距 Erican College", "dari Erican College", "من Erican College"]
out["View More"] = ["查看更多", "Lihat Lagi", "عرض المزيد"]
io.open(os.path.join(HERE, 'chunk6.json'), 'w', encoding='utf-8').write(
    json.dumps(out, ensure_ascii=False, indent=1))
print('chunk6.json: %d entries' % len(out))
