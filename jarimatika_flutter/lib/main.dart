import 'package:flutter/material.dart';
import 'screens/jarimatika_screen.dart';

void main() {
  runApp(const JarimatikaApp());
}

class JarimatikaApp extends StatelessWidget {
  const JarimatikaApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Jarimatika App',
      theme: ThemeData(
        primarySwatch: Colors.purple,
        fontFamily: 'Quicksand',
        useMaterial3: true,
      ),
      debugShowCheckedModeBanner: false,
      home: const JarimatikaScreen(),
    );
  }
}