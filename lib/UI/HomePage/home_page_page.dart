import 'package:camera_webview/UI/HomePage/home_page_cubit.dart';
import 'package:camera_webview/UI/HomePage/home_page_initial_params.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class HomePagePage extends StatefulWidget {
  final HomePageCubit cubit;
  // final UserDeInitialParams initialParams;
  const HomePagePage({Key? key, required this.cubit}) : super(key: key);

  @override
  State<HomePagePage> createState() => _HomePagePageState();
}

class _HomePagePageState extends State<HomePagePage> {
  HomePageCubit get cubit => widget.cubit;

  @override
  void initState() {
    super.initState();
    // TODO : Fix it Later
    cubit.onInit(HomePageInitialParams());
    cubit.navigator.context = context;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Exercise Options'),
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Center(
            child: ElevatedButton(
              onPressed: () {
                cubit.moveToPushUpScreen();
              },
              child: Text('Push Up'),
            ),
          ),
          SizedBox(
            height: 10,
          ),
          Center(
            child: ElevatedButton(
              onPressed: () {
                cubit.moveToPullUpScreen();
              },
              child: Text('Pull Up'),
            ),
          ),
          SizedBox(
            height: 10,
          ),
          Center(
              child: ElevatedButton(
                  onPressed: () {
                    cubit.moveToSquatScreen();
                  },
                  child: Text('Squat')))
        ],
      ),
    );
  }
}
