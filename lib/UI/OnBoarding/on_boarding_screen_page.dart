import 'package:camera_webview/UI/OnBoarding/on_boarding_screen_initial_params.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'on_boarding_screen_cubit.dart';

class OnBoardingScreenPage extends StatefulWidget {
  final OnBoardingScreenCubit cubit;
  // final UserDeInitialParams initialParams;
  const OnBoardingScreenPage({Key? key, required this.cubit}) : super(key: key);

  @override
  State<OnBoardingScreenPage> createState() => _OnBoardingScreenPageState();
}

class _OnBoardingScreenPageState extends State<OnBoardingScreenPage> {
  OnBoardingScreenCubit get cubit => widget.cubit;

  @override
  void initState() {
    super.initState();
    // TODO : Fix it Later
    cubit.onInit(OnBoardingScreenInitialParams());
    cubit.navigator.context = context;
  }

  @override
  Widget build(BuildContext context) {
    return
        // SafeArea(
        // child:

        Scaffold(
      appBar: AppBar(
        title: Text(''),
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          // Single onboarding page
          Center(
            child: OnboardingPage(
              title: 'Wellcome to Home GYM',
              description: 'We help you get a great physiue',
              imageUrl: '',
            ),
          ),

          // Skip button

          // Positioned(
          //   top: 40,
          //   right: 20,
          //   child: TextButton(
          //     onPressed: () {},
          //     child: Text(
          //       'Skip',
          //       style: TextStyle(fontSize: 16, color: Colors.grey[600]),
          //     ),
          //   ),
          // ),

          // Get Started button

          // Positioned(
          //   bottom: 40,
          //   left: 20,
          //   right: 20,
          //   child: ElevatedButton(
          //     onPressed: () {
          //       cubit.moveToHomePage();
          //     },
          //     style: ElevatedButton.styleFrom(
          //       primary: Colors.blue,
          //       padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
          //       shape: RoundedRectangleBorder(
          //         borderRadius: BorderRadius.circular(30),
          //       ),
          //     ),
          //     child: Text(
          //       'Get Started',
          //       style: TextStyle(fontSize: 18, color: Colors.white),
          //     ),
          //   ),
          // ),

          ElevatedButton(
            onPressed: () {
              cubit.moveToHomePage();
            },
            style: ElevatedButton.styleFrom(
              primary: Colors.blue,
              padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(30),
              ),
            ),
            child: Text(
              'Get Started',
              style: TextStyle(fontSize: 18, color: Colors.white),
            ),
          )
        ],
      ),
    );

    //     Scaffold(
    //     body:

    //     Column(
    //   children: [
    //     Text('Salam'),

    //   ],
    // )

    // );

    // );
  }
}

// import 'package:flutter/material.dart';

// void main() {
//   runApp(MyApp());
// }

// class MyApp extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       home: OnboardingScreen(),
//     );
//   }
// }

// class OnboardingScreen extends StatefulWidget {
//   @override
//   _OnboardingScreenState createState() => _OnboardingScreenState();
// }

// class _OnboardingScreenState extends State<OnboardingScreen> {
//   // final PageController _pageController = PageController();
//   int _currentPage = 0;

//   // Sample onboarding data
//   final List<Map<String, String>> onboardingData = [
//     {
//       'title': 'Welcome to the App!',
//       'description':
//           'Discover amazing features and start your journey with us.',
//       'image': 'https://via.placeholder.com/150', // Placeholder image
//     },
//     {
//       'title': 'Explore New Possibilities',
//       'description': 'Unlock a world of opportunities with our tools.',
//       'image': 'https://via.placeholder.com/150', // Placeholder image
//     },
//     {
//       'title': 'Get Started Now',
//       'description': 'Join our community and make the most of your experience.',
//       'image': 'https://via.placeholder.com/150', // Placeholder image
//     },
//   ];

//   @override
//   void dispose() {
//     // _pageController.dispose();
//     super.dispose();
//   }

//   void _onPageChanged(int index) {
//     setState(() {
//       // _currentPage = index;
//     });
//   }

//   void _skipToEnd() {
//     // _pageController.jumpToPage(onboardingData.length - 1);
//   }

//   void _getStarted() {
//     // Replace this with navigation to your main app screen
//     // Navigator.pushReplacement(
//     //   context,
//     //   MaterialPageRoute(builder: (context) => HomeScreen()),
//     // );
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       body: Stack(
//         children: [
//           // PageView for onboarding screens
//           // PageView.builder(
//           // controller: _pageController,
//           // onPageChanged: _onPageChanged,
//           // itemCount: onboardingData.length,
//           // itemBuilder: (context, index) {
//           // return
//           OnboardingPage(
//             title: onboardingData[0]['title']!,
//             description: onboardingData[0]['description']!,
//             imageUrl: onboardingData[0]['image']!,
//           ),
//           // },
//           // ),
//           // Skip button
//           Positioned(
//             top: 40,
//             right: 20,
//             child: TextButton(
//               onPressed: _skipToEnd,
//               child: Text(
//                 'Skip',
//                 style: TextStyle(fontSize: 16, color: Colors.grey[600]),
//               ),
//             ),
//           ),
//           // Page indicator and Get Started button
//           Positioned(
//             bottom: 40,
//             left: 20,
//             right: 20,
//             child: Column(
//               children: [
//                 // Page indicator dots
//                 // Row(
//                 //   mainAxisAlignment: MainAxisAlignment.center,
//                 //   children: List.generate(
//                 //     onboardingData.length,
//                 //     (index) => AnimatedContainer(
//                 //       duration: Duration(milliseconds: 300),
//                 //       margin: EdgeInsets.symmetric(horizontal: 5),
//                 //       height: 8,
//                 //       width: _currentPage == index ? 24 : 8,
//                 //       decoration: BoxDecoration(
//                 //         color:
//                 //             _currentPage == index ? Colors.blue : Colors.grey,
//                 //         borderRadius: BorderRadius.circular(4),
//                 //       ),
//                 //     ),
//                 //   ),
//                 // ),

//                 SizedBox(height: 20),
//                 // Get Started button on last page
//                 // if (_currentPage == onboardingData.length - 1)

//                 ElevatedButton(
//                   onPressed: _getStarted,
//                   style: ElevatedButton.styleFrom(
//                     primary: Colors.blue,
//                     padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
//                     shape: RoundedRectangleBorder(
//                       borderRadius: BorderRadius.circular(30),
//                     ),
//                   ),
//                   child: Text(
//                     'Get Started',
//                     style: TextStyle(fontSize: 18, color: Colors.white),
//                   ),
//                 ),
//               ],
//             ),
//           ),
//         ],
//       ),
//     );
//   }
// }

// import 'package:flutter/material.dart';

// void main() {
//   runApp(MyApp());
// }

// class MyApp extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       home: OnboardingScreen(),
//     );
//   }
// }

// class OnboardingScreen extends StatefulWidget {
//   @override
//   _OnboardingScreenState createState() => _OnboardingScreenState();
// }

// class _OnboardingScreenState extends State<OnboardingScreen> {
//   // Single onboarding data
//   final Map<String, String> onboardingData = {
//     'title': 'Welcome to the App!',
//     'description': 'Discover amazing features and start your journey with us.',
//     'image': 'https://via.placeholder.com/150', // Placeholder image
//   };

//   void _skipToEnd() {
//     // Replace with your skip logic (e.g., navigate to main screen)
//     // Navigator.pushReplacement(
//     //   context,
//     //   MaterialPageRoute(builder: (context) => HomeScreen()),
//     // );
//   }

//   void _getStarted() {
//     // Replace with navigation to your main app screen
//     // Navigator.pushReplacement(
//     //   context,
//     //   MaterialPageRoute(builder: (context) => HomeScreen()),
//     // );
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       body: Column(
//         children: [
//           // Single onboarding page
//           // OnboardingPage(
//           //   title: onboardingData['title']!,
//           //   description: onboardingData['description']!,
//           //   imageUrl: onboardingData['image']!,
//           // ),

//           // Skip button
//           Positioned(
//             top: 40,
//             right: 20,
//             child: TextButton(
//               onPressed: () {},
//               child: Text(
//                 'Skip',
//                 style: TextStyle(fontSize: 16, color: Colors.grey[600]),
//               ),
//             ),
//           ),
//           // Get Started button
//           Positioned(
//             bottom: 40,
//             left: 20,
//             right: 20,
//             child: ElevatedButton(
//               onPressed: _getStarted,
//               style: ElevatedButton.styleFrom(
//                 primary: Colors.blue,
//                 padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
//                 shape: RoundedRectangleBorder(
//                   borderRadius: BorderRadius.circular(30),
//                 ),
//               ),
//               child: Text(
//                 'Get Started',
//                 style: TextStyle(fontSize: 18, color: Colors.white),
//               ),
//             ),
//           ),
//         ],
//       ),
//     );
//   }
// }

// // Single onboarding page widget
// class OnboardingPage extends StatelessWidget {
//   final String title;
//   final String description;
//   final String imageUrl;

//   OnboardingPage({
//     required this.title,
//     required this.description,
//     required this.imageUrl,
//   });

//   @override
//   Widget build(BuildContext context) {
//     return Padding(
//       padding: const EdgeInsets.all(20.0),
//       child: Column(
//         mainAxisAlignment: MainAxisAlignment.center,
//         children: [
//           // Image.network(
//           //   imageUrl,
//           //   height: 200,
//           //   fit: BoxFit.cover,
//           // ),
//           SizedBox(height: 40),
//           Text(
//             title,
//             style: TextStyle(
//               fontSize: 24,
//               fontWeight: FontWeight.bold,
//               color: Colors.black87,
//             ),
//             textAlign: TextAlign.center,
//           ),
//           SizedBox(height: 20),
//           Text(
//             description,
//             style: TextStyle(
//               fontSize: 16,
//               color: Colors.grey[600],
//             ),
//             textAlign: TextAlign.center,
//           ),
//         ],
//       ),
//     );
//   }
// }

// // Placeholder HomeScreen for navigation
// class HomeScreen extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(title: Text('Home')),
//       body: Center(child: Text('Welcome to the Home Screen!')),
//     );
//   }
// }

// Single onboarding page widget
class OnboardingPage extends StatelessWidget {
  final String title;
  final String description;
  final String imageUrl;

  OnboardingPage({
    required this.title,
    required this.description,
    required this.imageUrl,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // Image.network(
          //   imageUrl,
          //   height: 200,
          //   fit: BoxFit.cover,
          // ),
          SizedBox(height: 40),
          Text(
            title,
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Colors.black87,
            ),
            textAlign: TextAlign.center,
          ),
          SizedBox(height: 20),
          Text(
            description,
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey[600],
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}

// Placeholder HomeScreen for navigation
// class HomeScreen extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(title: Text('Home')),
//       body: Center(child: Text('Welcome to the Home Screen!')),
//     );
//   }
// }
