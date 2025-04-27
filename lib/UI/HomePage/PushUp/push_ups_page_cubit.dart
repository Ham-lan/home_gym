import 'package:camera_webview/UI/HomePage/PushUp/push_ups_page_navigator.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'push_ups_page_initial_params.dart';
import 'push_ups_page_state.dart';

class PushUpsPageCubit extends Cubit<PushUpsPageState> {
  final PushUpsPageInitialParams initialParams;
  final PushUpsPageNavigator navigator;
  PushUpsPageCubit(this.initialParams, this.navigator)
      : super(PushUpsPageState.initial(initialParams: initialParams));

  void onInit(PushUpsPageInitialParams initialParams) => emit(state.copyWith());
}
