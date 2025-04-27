import 'package:camera_webview/UI/HomePage/Squat/squats_page_page.dart';
import 'package:flutter/material.dart';

import '../../../Navigation/navigator.dart';
import '../../../main.dart';
import 'squats_page_initial_params.dart';

class SquatsPageNavigator with SquatsPageRoute {
  SquatsPageNavigator(this.navigator);
  @override
  // TODO: implement context
  late BuildContext context;

  @override
  // TODO: implement navigator
  AppNavigator navigator;
}

mixin SquatsPageRoute {
  openSquatsPagePage(SquatsPageInitialParams initialParams) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => SquatsPagePage(
              cubit: getIt(param1: initialParams),
            )));
  }

  BuildContext get context;
  AppNavigator get navigator;
}
