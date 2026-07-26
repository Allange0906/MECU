import 'dart:convert';
import 'package:http/http.dart' as http;

class MecuService {
  static const String _baseUrl = String.fromEnvironment(
    'MECU_API_URL',
    defaultValue: 'http://127.0.0.1:5050/predict',
  );

  // 서버에서 원-핫 인코딩을 적용하므로 앱은 원본 범주값을 그대로 전송한다.
  Future<List<dynamic>> predictFood({
    required String time,
    required String place,
    required String companion,
    required List<String> categories,
    required int spice,
    required String price,
    String naturalText = '',
    double temperature = 1.0,
  }) async {
    try {
      final response = await http.post(
        Uri.parse(_baseUrl),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "time": time,
          "place": place,
          "companion": companion,
          "categories": categories,
          "spice": spice,
          "price": price,
          "naturalText": naturalText,
          "temperature": temperature,
        }),
      );

      final decodedBody = utf8.decode(response.bodyBytes);

      if (response.statusCode != 200) {
        throw Exception('서버 응답 오류 ${response.statusCode}: $decodedBody');
      }

      if (decodedBody.trim().isEmpty) {
        throw Exception('서버가 빈 응답을 반환했습니다.');
      }

      final decodedJson = jsonDecode(decodedBody);
      if (decodedJson is List) {
        return decodedJson;
      }

      throw Exception('추천 리스트가 아닌 응답입니다: $decodedBody');
    } catch (e) {
      throw Exception('추천 요청 실패: $e');
    }
  }
}
