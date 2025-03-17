Below is a self-reflection I have submitted to the course provider after completing the project, which I believe will help provide background for this repository.

Reflection:

The three API providers mentioned in this tutorial require either credit card information or payment, so I opted for the free version from ‘https://www.voicerss.org' as suggested by another student.

To determine if this API is suitable for my needs, I reviewed the API documentation and tested the API URL in the Postman app before registering as a new user.

I then drafted the initial code, including the .env file, imports, global variables, and Tkinter setup. Once done, I forwarded the draft to ChatGPT for a quick review and suggestions.

While reviewing the API documentation, I discovered that another parameter needed to be added to specify the correct file format (e.g., MP3). After this update, the app’s text-to-speech functionality finally worked.

With the help of ChatGPT, the next step I took was to consider how to improve the layout/design of the app:

* Button with a microphone icon
* Change in the height and width of the Tkinter window, font size, and title
* Building a script that takes a PDF file, identifies the text, and passes the text to the text block or directly to the API’s ‘src’ parameter
* A new feature allowing users to select a PDF file from their local system
* A new feature allowing users to select different languages

The most important bug I encountered was with the URL parameter, which seemed to be incorrect after adding the language selection feature. For example, once I extracted the text from a PDF file, the code failed to run the API when I selected one of the languages from the drop-down menu. To resolve this, I used a simple ‘print’ technique, where the IDE prints the entire URL being passed to the API. Here, I discovered that one of the parameters, such as the actual language code (e.g., ‘zh-cn’), was not being passed; instead, the language name (e.g., ‘Chinese (China)’) was being passed.

After fixing the issue, I asked a friend who is a backend developer to review the code. This was a very useful exercise, as my friend showed me how he would organise the code across different files, rather than keeping it all in one file as I had done.

The app can still be improved, but I believe I have covered everything in this challenge. This time, I spent a little more time planning the overall structure of the app at the beginning before diving into the coding.
