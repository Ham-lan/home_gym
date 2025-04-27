import 'package:camera_webview/UI/HomePage/Squat/squats_page_navigator.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'squats_page_initial_params.dart';
import 'squats_page_state.dart';

class SquatsPageCubit extends Cubit<SquatsPageState> {
  final SquatsPageInitialParams initialParams;
  final SquatsPageNavigator navigator;
  SquatsPageCubit(this.initialParams, this.navigator)
      : super(SquatsPageState.initial(initialParams: initialParams));

  void onInit(SquatsPageInitialParams initialParams) => emit(state.copyWith());
}
