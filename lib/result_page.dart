import 'package:flutter/material.dart';

class ResultPage extends StatelessWidget {
  final List<dynamic> recommendations; // 서버에서 받을 데이터 (rank, name, prob 포함)

  const ResultPage({super.key, required this.recommendations});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          '메추 추천 결과',
          style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
        ),
        backgroundColor: Colors.orange,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "메추가 추천하는 메뉴는?",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            
            // 1. 결과 리스트 표시 (Expanded로 감싸서 남은 공간 차지)
            Expanded(
              child: recommendations.isEmpty // 추천 결과 없냐?
                  ? const Center(child: Text("추천 결과가 없습니다."))
                  : ListView.builder( // 리스트의 시각화
                      itemCount: recommendations.length,
                      itemBuilder: (context, index) {
                        final item = recommendations[index];
                        return _buildResultCard(
                          rank: item['rank'].toString(), // 1 ~ 5순위
                          name: item['name'], // 음식 이름
                          probability: item['prob'], // 추천율
                        );
                      },
                    ),
            ),
            
            const SizedBox(height: 20),
            
            // 2. 다시 선택하기 버튼
            SizedBox(
              width: double.infinity,
              height: 55,
              child: ElevatedButton(
                onPressed: () => Navigator.pop(context),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.grey[200],
                  foregroundColor: Colors.black,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                ),
                child: const Text("다시 선택하기", style: TextStyle(fontSize: 16)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // 메뉴 하나하나를 보여주는 카드 위젯
  Widget _buildResultCard({required String rank, required String name, required String probability}) {
    return Container(
      margin: const EdgeInsets.only(bottom: 15),
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: rank == "1" 
        ? Colors.orange.withValues(alpha: 0.1) : rank == "2" ? Colors.orange.withValues(alpha: 0.06) : rank == "3" ? Colors.orange.withValues(alpha: 0.03) : Colors.white,
        borderRadius: BorderRadius.circular(15),
        border: Border.all(
          color: rank == "1" ? Colors.orange : rank == "2" ? Colors.orange.withValues(alpha: 0.8) : rank == "3" ? Colors.orange.withValues(alpha: 0.6) : Colors.grey.withValues(alpha: 0.3),
        ),
      ),
      child: Row(
        children: [
          // 순위 아이콘
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: rank == "1" ? Colors.orange : rank == "2" ? Colors.orange.withValues(alpha: 0.8) : rank == "3" ? Colors.orange.withValues(alpha: 0.6) : Colors.grey[400],
              shape: BoxShape.circle,
            ),
            alignment: Alignment.center,
            child: Text(
              rank,
              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
            ),
          ),
          const SizedBox(width: 15),
          // 음식 이름
          Expanded(
            child: Text(
              name,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          ),
          // 확률 표시
          Text(
            probability,
            style: const TextStyle(
              color: Colors.orange,
              fontWeight: FontWeight.bold,
              fontSize: 16,
            ),
          ),
        ],
      ),
    );
  }
}