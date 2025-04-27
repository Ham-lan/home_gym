import 'package:camera_webview/UI/HomePage/PullUp/pull_ups_page_navigator.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'pull_ups_page_initial_params.dart';
import 'pull_ups_page_state.dart';

class PullUpsPageCubit extends Cubit<PullUpsPageState> {
  final PullUpsPageInitialParams initialParams;
  final PullUpsPageNavigator navigator;
  PullUpsPageCubit(this.initialParams, this.navigator)
      : super(PullUpsPageState.initial(initialParams: initialParams));

  void onInit(PullUpsPageInitialParams initialParams) => emit(state.copyWith());
}
