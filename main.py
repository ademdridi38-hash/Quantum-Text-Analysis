import requests
import re
import numpy as np
import matplotlib.pyplot as plt

class YasminaQuantumLab:
    def __init__(self):
        # استخدام النسخة البسيطة لضمان دقة البحث الرياضي
        self.api_url = "https://api.alquran.cloud/v1/quran/quran-simple"
        self.data = self._fetch_data()

    def _fetch_data(self):
        """سحب البيانات الخام من السيرفر"""
        try:
            print("📡 Connecting to Quantum Data Stream...")
            response = requests.get(self.api_url, timeout=20)
            return response.json()['data']['surahs']
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return []

    def super_normalize(self, text):
        """تجريد النص من الضجيج (التشكيل، الهمزات، والياءات)"""
        if not text: return ""
        # إزالة التشكيل وكل ما ليس حرفاً أساسياً
        text = re.sub(r'[^\u0621-\u064A]', '', text) 
        # توحيد الألف (أإآ -> ا) والياء (ى -> ي)
        text = re.sub(r'[أإآ]', 'ا', text)
        text = re.sub(r'[ىي]', 'ي', text)
        return text

    def analyze_system(self, target_word):
        """تحليل المسافات الهندسية والإحصائية لنظام معين"""
        if not self.data: return None

        print(f"🔬 Scanning for System: {target_word}...")
        global_index = 0
        positions = []
        target = self.super_normalize(target_word)

        for surah in self.data:
            for ayah in surah['ayahs']:
                words = ayah['text'].split()
                for word in words:
                    global_index += 1
                    if target in self.super_normalize(word):
                        positions.append(global_index)

        if len(positions) < 2:
            return None

        # حساب المسافات (Spacings)
        spacings = [positions[i] - positions[i-1] for i in range(1, len(positions))]
        
        return {
            "name": target_word,
            "count": len(positions),
            "spacings": spacings,
            "avg": np.mean(spacings),
            "cv": np.std(spacings) / np.mean(spacings)
        }

    def run_comparison(self, system_a, system_b):
        """إجراء المقارنة الكبرى بين نظامين"""
        res_a = self.analyze_system(system_a)
        res_b = self.analyze_system(system_b)

        if not res_a or not res_b:
            print("⚠️ Data insufficient for comparison.")
            return

        # 1. التقرير النصي الموحد
        print("\n" + "="*50)
        print(f"{'Metric':<20} | {res_a['name']:<12} | {res_b['name']:<12}")
        print("-" * 50)
        print(f"{'Occurrences':<20} | {res_a['count']:<12} | {res_b['count']:<12}")
        print(f"{'Mean Wavelength':<20} | {res_a['avg']:<12.2f} | {res_b['avg']:<12.2f}")
        print(f"{'Symmetry (CV)':<20} | {res_a['cv']:<12.4f} | {res_b['cv']:<12.4f}")
        print("="*50)

        # 2. الرسم البياني المقارن
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=False)
        fig.subplots_adjust(hspace=0.4)

        # نظام أ (ابراهيم)
        ax1.stem(res_a['spacings'], linefmt='b-', markerfmt='bo', basefmt='r-')
        ax1.set_title(f"System Pulse: {res_a['name']} (Resonance)")
        ax1.set_ylabel("Distance (Words)")

        # نظام ب (موسى)
        ax2.stem(res_b['spacings'], linefmt='g-', markerfmt='go', basefmt='r-')
        ax2.set_title(f"System Pulse: {res_b['name']} (High Frequency)")
        ax2.set_ylabel("Distance (Words)")
        ax2.set_xlabel("Sequence of Occurrence")

        plt.show()

# --- انطلاق المختبر ---
if __name__ == "__main__":
    lab = YasminaQuantumLab()
    # تشغيل المقارنة الكبرى بين ابراهيم وموسى
    lab.run_comparison("ابراهيم", "موسى")