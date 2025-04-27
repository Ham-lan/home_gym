import 'package:camera_webview/UI/HomePage/PullUp/pull_ups_page_page.dart';
import 'package:flutter/material.dart';

import '../../../Navigation/navigator.dart';
import '../../../main.dart';
import 'pull_ups_page_initial_params.dart';

class PullUpsPageNavigator with PullUpsPageRoute {
  PullUpsPageNavigator(this.navigator);
  @override
  // TODO: implement context
  late BuildContext context;

  @override
  // TODO: implement navigator
  AppNavigator navigator;
}

mixin PullUpsPageRoute {
  openPullUpsPagePage(PullUpsPageInitialParams initialParams) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => PullUpsPagePage(
              cubit: getIt(param1: initialParams),
            )));
  }

  BuildContext get context;
  AppNavigator get navigator;
}
