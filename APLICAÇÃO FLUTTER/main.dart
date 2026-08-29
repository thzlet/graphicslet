/* 
questão 3

essa eh uma aplicação flutter usando um StatefulWidget porque preciso alterar o estado da tela. 
tem uma lista com oito cores e uso um GridView para apresentar essas cores em uma grade. 
cada quadrado possui um GestureDetector, que identifica quando o usuário clica nele.
qdo clica, a função _selecionarCor é chamada e utiliza setState para atualizar a variável _corFundo. 
o Scaffold utiliza essa variável como sua cor de fundo, então a tela muda automaticamente. 
também implementei uma função que calcula a luminância da cor para escolher entre texto preto ou branco ;)

*/

import 'package:flutter/material.dart'; // biblioteca com alguns materiais de interface do flutter 

void main() { // ponto inicial do programa
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cores de Fundo',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(useMaterial3: true),
      home: const TelaCores(), 
    );
  }
}

class TelaCores extends StatefulWidget { // controla a mudança de cores
  const TelaCores({super.key});

  @override
  State<TelaCores> createState() => _TelaCoresState();
}

class _TelaCoresState extends State<TelaCores> {
  // fundo da tela
  Color _corFundo = Colors.white;

  // quadrados clicáveis
  final List<Color> _paleta = const [
    Color(0xFFE53935), // vermelho
    Color(0xFF43A047), // verde
    Color(0xFF1E88E5), // azul
    Color(0xFFFDD835), // amarelo
    Color(0xFF8E24AA), // roxo
    Color(0xFF00ACC1), // ciano
    Color(0xFFFB8C00), // laranja
    Color(0xFF546E7A), // cinza 
  ];

  void _selecionarCor(Color cor) {
    setState(() {
      _corFundo = cor;
    });
  }

  // escolhe cor do texto (preto/branco) 
  Color _corContraste(Color fundo) {
    final luminancia = fundo.computeLuminance();
    return luminancia > 0.5 ? Colors.black : Colors.white;
  }

  @override
  Widget build(BuildContext context) {
    final corTexto = _corContraste(_corFundo);

    return Scaffold(
      backgroundColor: _corFundo,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start, // alinha os elementos da coluna
            children: [
              Text(
                'Toque em um quadrado\npara mudar o fundo',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                  color: corTexto,
                ),
              ),
              const SizedBox(height: 24),
              Expanded(
                child: GridView.count(
                  crossAxisCount: 4, // define 4 colunas na grade 
                  crossAxisSpacing: 12, // pixels de espaço entre os quadrados 
                  mainAxisSpacing: 12,
                  children: _paleta.map((cor) {
                    return GestureDetector(
                      onTap: () => _selecionarCor(cor),
                      child: Container(
                        decoration: BoxDecoration(
                          color: cor,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(
                            color: cor == _corFundo ? corTexto : Colors.transparent,
                            width: 3,
                          ),
                          boxShadow: const [
                            BoxShadow(
                              color: Colors.black26,
                              blurRadius: 6,
                              offset: Offset(0, 3),
                            ),
                          ],
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}