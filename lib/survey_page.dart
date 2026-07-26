import 'package:flutter/material.dart';
import 'result_page.dart';
import 'services/mecu_service.dart';

void main() {
  runApp(const MaterialApp(
    home: SurveyPage(),
    debugShowCheckedModeBanner: false,
  ));
}

class SurveyPage extends StatefulWidget {
  const SurveyPage({super.key});

  @override
  State<SurveyPage> createState() => _SurveyPageState();
}

class _SurveyPageState extends State<SurveyPage> {
  final TextEditingController _naturalTextController = TextEditingController();

  // [1] 선택된 시간대 저장 변수 (단일 선택용)
  String? _selectedTime;
  final List<String> _timeOptions = ['아침', '점심', '저녁', '간식', '야식'];

  // [2] 선택된 장소 선택 저장 변수 (단일 선택용)
  String? _selectedPlace;
  final List<String> _placeOptions = ['집밥', '배달', '외식'];

  // [3] 선택된 동석자 선택 저장 변수 (단일 선택용)
  String? _selectedCompanion;
  final List<String> _companionOptions = ['혼밥', '데이트', '가족식사', '모임', '남자끼리', '여자끼리'];

  // [4] 선택된 카테고리 저장 변수 (복수 선택용)
  final List<String> _selectedCategories = [];
  final List<String> _categoryOptions = ['한식', '중식', '일식', '양식', '남아시아', '동남아시아'];

  // [5] 매운맛 단계 지수 (0 ~ 5단계)
  double _spiceValue = 0;
  double _temperatureValue = 1.0;

  // [5-1] 매운맛 단계에 따른 예시 음식 리스트 반환 함수
  List<String> _getFoodExamples(double score) {
    int level = score.toInt();
    if (level == 0) return ["짜장면", "간장계란밥", "불고기"];
    if (level == 1) return ["너구리", "제육볶음", "오징어짬뽕"];
    if (level == 2) return ["신라면", "왕뚜껑", "진라면 매운맛"];
    if (level == 3) return ["열라면", "불닭볶음면", "엽기떡볶이 3단계"];
    if (level == 4) return ["신라면 레드", "매운 닭발", "틈새라면"];
    return ["핵불닭볶음면", "틈새라면 빨계떡", "엽기떡볶이 5단계"];
  }

  // [6] 선택된 1인당 가격 저장 변수 (단일 선택용)
  String? _selectedPrice;
  final List<String> _priceOptions = ['1만원 이하', '1~2만원', '2~3만원', '3만원 이상'];

  @override
  void dispose() {
    _naturalTextController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          '메추',
          style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
        ),
        backgroundColor: Colors.orange,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // [1] 식사 시간 섹션
            _buildSelectionSection(
              title: "식사 시간",
              icon: Icons.access_time_filled,
              options: _timeOptions,
              selectedValues: _selectedTime,
              onSelected: (value) {
                setState(() {
                  _selectedTime = (_selectedTime == value) ? null : value; // 토글 기능
                });
              },
            ),
            
            const SizedBox(height: 30),

            // [2] 장소 섹션
            _buildSelectionSection(
              title: "식사 장소",
              icon: Icons.place, 
              options: _placeOptions,
              selectedValues: _selectedPlace,
              onSelected: (value) {
                setState(() {
                  _selectedPlace = (_selectedPlace == value) ? null : value; // 토글 기능
                });
              },
            ),

            const SizedBox(height: 30),

            // [3] 동석자 섹션
            _buildSelectionSection(
              title: "동석자",
              icon: Icons.people, 
              options: _companionOptions,
              selectedValues: _selectedCompanion,
              onSelected: (value) {
                setState(() {
                  _selectedCompanion = (_selectedCompanion == value) ? null : value; // 토글 기능
                });
              },
            ),

            const SizedBox(height: 30),

            // [4] 카테고리 섹션
            _buildSelectionSection(
              title: "선호하는 카테고리",
              icon: Icons.restaurant_menu,
              options: _categoryOptions,
              selectedValues: _selectedCategories,
              onSelected: (value) {
                setState(() {
                  // 리스트(복수)를 받기 때문에 _selectedCategories(선택된 카테고리 리스트)에 추가/제거 기능
                  if (_selectedCategories.contains(value)) {
                    _selectedCategories.remove(value); // 토글
                  } else {
                    _selectedCategories.add(value); // 토글
                  }
                });
              },
            ),
            const SizedBox(height: 10),
            const Text(
              "카테고리는 복수 선택이 가능합니다.\n"
              "치킨은 양식으로 분류하였고 떡볶이는 한식으로 분류하였습니다.",
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),

            const SizedBox(height: 30),

            // [5] 매운맛 섹션
            _buildSpicinessSection(), // 매운맛 슬라이더
            const SizedBox(height: 10),
            const Text(
              "치킨은 후라이드와 양념을 포함하기에 0 ~ 2단계,\n"
              "떡볶이는 가게와 프랜차이즈 간의 차이를 고려해 2 ~ 5단계 사이입니다.",
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),

            const SizedBox(height: 30),

            // [6] 가격 섹션
            _buildSelectionSection(
              title: "1인당 가격 (선택)",
              icon: Icons.credit_card, 
              options: _priceOptions,
              selectedValues: _selectedPrice,
              onSelected: (value) {
                setState(() {
                  _selectedPrice = (_selectedPrice == value) ? null : value; // 토글 기능
                });
              },
            ),

            const SizedBox(height: 10),
            const Text(
              "가격은 1인당 기준이며, 선택하지 않으면 가격이 낮은 순서로 처리됩니다.",
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),

            const SizedBox(height: 30),

            _buildNaturalLanguageSection(),

            const SizedBox(height: 30),

            _buildTemperatureSection(),

            const SizedBox(height: 50),

            // 메뉴 추천 받기 버튼
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                // 시간, 장소, 동석자는 필수 / 가격은 선택(없어도 됨)
                onPressed:
                    (_selectedTime != null &&
                        _selectedPlace != null &&
                        _selectedCompanion != null &&
                        _selectedCategories.isNotEmpty)
                    ? () async {
                        final mecuService = MecuService();

                        try {
                          showDialog(
                            context: context,
                            barrierDismissible: false,
                            builder: (context) => const Center(
                              child: CircularProgressIndicator(
                                color: Colors.orange,
                              ),
                            ),
                          );

                          final List<dynamic> results = await mecuService
                              .predictFood(
                                time: _selectedTime!,
                                place: _selectedPlace!,
                                companion: _selectedCompanion!,
                                categories: _selectedCategories,
                                spice: _spiceValue.toInt(),
                                price: _selectedPrice ?? '상관없음',
                                naturalText: _naturalTextController.text,
                                temperature: _temperatureValue,
                              );

                          if (!mounted) return;
                          Navigator.of(context, rootNavigator: true).pop();

                          if (results.isNotEmpty) {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => ResultPage(
                                  recommendations: results,
                                ),
                              ),
                            );
                          } else {
                            _showErrorSnackBar("추천 결과를 가져오지 못했습니다.");
                          }
                        } catch (e) {
                          if (mounted) {
                            Navigator.of(context, rootNavigator: true).pop();
                            _showErrorSnackBar(e.toString());
                          }
                        }
                      }
                    : null,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.orange,
                  foregroundColor: Colors.white,
                ),
                child: const Text("메뉴 추천 받기", style: TextStyle(fontSize: 18)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // 에러 스낵바 표시 함수
  void _showErrorSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: Colors.red),
    );
  }
  // 선택 섹션 빌더
  Widget _buildSelectionSection({
    required String title,
    required List<String> options,
    required dynamic selectedValues,
    required Function(String) onSelected,
    required IconData icon,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, color: Colors.orange, size: 24),
            const SizedBox(width: 8),
            Text(
              title,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ],
        ),
        const SizedBox(height: 15),
        Wrap(
          spacing: 10.0,
          runSpacing: 10.0,
          children: options.map((option) {
            final isSelected = (selectedValues is List)
                ? selectedValues.contains(option)
                : selectedValues == option;
            // 리스트(복수)냐 단일값이냐에 따라 선택 여부 판단

            return ChoiceChip(
              label: Text(
                option,
                style: TextStyle(
                  color: isSelected ? Colors.white : Colors.black,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
              ),
              selected: isSelected,
              selectedColor: Colors.orange,
              backgroundColor: Colors.grey[200],
              onSelected: (selected) {
                onSelected(option);
              },
            );
          }).toList(),
        ),
      ],
    );
  }

  // 매운맛 슬라이더 섹션 빌더
  Widget _buildSpicinessSection() {
    // 현재 _spiceValue에 맞는 예시 음식 리스트 가져오기
    List<String> examples = _getFoodExamples(_spiceValue);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(Icons.local_fire_department, color: Colors.orange),
            const SizedBox(width: 8),
            const Text(
              "맵기",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ],
        ),
        const SizedBox(height: 10),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween, // 양 끝 정렬(순한 맛<->매운 맛)
          children: [
            const Text("순한 맛"),
            Text(
              "${_spiceValue.toInt()}단계",
              style: const TextStyle(
                color: Colors.orange,
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
            const Text("매운 맛"),
          ],
        ),
        SliderTheme(
          data: SliderTheme.of(context).copyWith(
            tickMarkShape: SliderTickMarkShape.noTickMark, // 분할점 없애기
            activeTrackColor: Colors.orange, // 채워진 트랙 색
            thumbColor: Colors.orange, 
            valueIndicatorColor: Colors.orange, 
          ),
          child: Slider(
            value: _spiceValue,
            min: 0,
            max: 5,
            divisions: 5,
            label: "${_spiceValue.toInt()}단계",
            onChanged: (double value) {
              setState(() {
                _spiceValue = value; // 슬라이더 움직이면 _spiceValue 갱신
              });
            },
          ),
        ),
        const SizedBox(height: 10),
        // 예시 박스
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(15),
          decoration: BoxDecoration(
            color: Colors.orange.withValues(alpha: 0.2),
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: Colors.orange, width: 1.5),
          ),
          child: Column(
            children: [
              Text(
                "🔥 ${_spiceValue.toInt()}단계 수준의 음식 🔥",
                style: const TextStyle(
                  color: Colors.orange,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                examples.join(", "),
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildNaturalLanguageSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(Icons.chat_bubble, color: Colors.orange),
            const SizedBox(width: 8),
            const Text(
              "세부사항",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ],
        ),
        const SizedBox(height: 12),
        TextField(
          controller: _naturalTextController,
          keyboardType: TextInputType.multiline,
          textInputAction: TextInputAction.newline,
          enableInteractiveSelection: true,
          minLines: 2,
          maxLines: 3,
          decoration: InputDecoration(
            hintText: "예: 오늘 비 오고 추워서 얼큰한 국물 요리가 먹고 싶어",
            hintStyle: TextStyle(color: Colors.grey[700]),
            filled: true,
            fillColor: Colors.grey[100],
            suffixIcon: IconButton(
              icon: const Icon(Icons.clear),
              color: Colors.grey,
              tooltip: "입력 지우기",
              onPressed: () {
                _naturalTextController.clear();
              },
            ),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
              borderSide: BorderSide(color: Colors.grey.withValues(alpha: 0.18)),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
              borderSide: BorderSide(color: Colors.grey.withValues(alpha: 0.18)),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
              borderSide: const BorderSide(color: Colors.orange, width: 1),
            ),
          ),
        ),
        const SizedBox(height: 8),
        const Text(
          "문장 속 국물, 얼큰, 매운, 비 같은 키워드를 서버에서 추천 피처로 변환합니다.",
          style: TextStyle(fontSize: 15, color: Colors.grey),
        ),
      ],
    );
  }

  Widget _buildTemperatureSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(Icons.tune, color: Colors.orange),
            const SizedBox(width: 8),
            const Text(
              "추천 다양성",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ],
        ),
        const SizedBox(height: 10),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text("정확도 우선"),
            Text(
              _temperatureValue.toStringAsFixed(1),
              style: const TextStyle(
                color: Colors.orange,
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
            const Text("다양성 우선"),
          ],
        ),
        SliderTheme(
          data: SliderTheme.of(context).copyWith(
            tickMarkShape: SliderTickMarkShape.noTickMark,
            activeTrackColor: Colors.orange,
            thumbColor: Colors.orange,
            valueIndicatorColor: Colors.orange,
          ),
          child: Slider(
            value: _temperatureValue,
            min: 0.5,
            max: 2.0,
            divisions: 15,
            label: _temperatureValue.toStringAsFixed(1),
            onChanged: (double value) {
              setState(() {
                _temperatureValue = value;
              });
            },
          ),
        ),
        const Text(
          "Temperature Scaling으로 낮은 값은 확정적인 추천, 높은 값은 다양한 추천을 만듭니다.",
          style: TextStyle(fontSize: 15, color: Colors.grey),
        ),
      ],
    );
  }
}
