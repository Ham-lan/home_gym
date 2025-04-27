import 'package:camera_webview/UI/HomePage/PullUp/pull_ups_page_initial_params.dart';
import 'package:camera_webview/UI/HomePage/PushUp/push_ups_page_initial_params.dart';
import 'package:camera_webview/UI/HomePage/Squat/squats_page_initial_params.dart';
import 'package:camera_webview/UI/HomePage/home_page_navigator.dart';
import 'package:camera_webview/UI/HomePage/home_page_state.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'home_page_initial_params.dart';

class HomePageCubit extends Cubit<HomePageState> {
  final HomePageInitialParams initialParams;
  final HomePageNavigator navigator;
  HomePageCubit(this.initialParams, this.navigator)
      : super(HomePageState.initial(initialParams: initialParams));

  void onInit(HomePageInitialParams initialParams) => emit(state.copyWith());

  void moveToPushUpScreen() {
    navigator.openPushUpsPagePage(PushUpsPageInitialParams());
  }

  void moveToPullUpScreen() {
    navigator.openPullUpsPagePage(PullUpsPageInitialParams());
  }

  void moveToSquatScreen() {
    navigator.openSquatsPagePage(SquatsPageInitialParams());
  }
}
