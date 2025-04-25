import 'package:camera_webview/UI/Splash%20Screen/splash_screen_initial_params.dart';
import 'package:camera_webview/UI/Splash%20Screen/splash_screen_navigator.dart';
import 'package:camera_webview/UI/Splash%20Screen/splash_screen_state.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class SplashScreenCubit extends Cubit<SplashScreenState> {
  final SplashScreenInitialParams initialParams;
  final SplashScreenNavigator navigator;
  SplashScreenCubit(this.initialParams, this.navigator)
      : super(SplashScreenState.initial(initialParams: initialParams));

  void onInit(SplashScreenInitialParams initialParams) =>
      emit(state.copyWith());
}
