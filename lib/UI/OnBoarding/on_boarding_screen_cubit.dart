import 'package:camera_webview/UI/HomePage/home_page_initial_params.dart';
import 'package:camera_webview/UI/OnBoarding/on_boarding_screen_navigator.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'on_boarding_screen_initial_params.dart';
import 'on_boarding_screen_state.dart';

class OnBoardingScreenCubit extends Cubit<OnBoardingScreenState> {
  final OnBoardingScreenInitialParams initialParams;
  final OnBoardingScreenNavigator navigator;
  OnBoardingScreenCubit(this.initialParams, this.navigator)
      : super(OnBoardingScreenState.initial(initialParams: initialParams));

  void onInit(OnBoardingScreenInitialParams initialParams) =>
      emit(state.copyWith());

  void moveToHomePage() {
    navigator.openHomePagePage(HomePageInitialParams());
  }
}
