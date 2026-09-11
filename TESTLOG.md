# Test LOG
Test to see how LLM response to our question with/without data in documents that we've ingested! 

## Test with QUESTION that have answer in our documents
### Qestion 1: How to setup email for mobile devices?
```
[-] You: How to setup email for mobile devices?

TOP_K Chunk : [4]
================================================================================
source                                                           distance   rank
001_Setting_Up_a_Mobile_Device_for_Company_Email.txt               0.2941      1
010_Configuring_Email_on_an_Android_Device.txt                     0.3485      2
001_Setting_Up_a_Mobile_Device_for_Company_Email.txt               0.3587      3
010_Configuring_Email_on_an_Android_Device.txt                     0.4235      4

[+] Assistant: To set up email for mobile devices, follow these steps:

**For iOS, Android, or Windows devices:**

1. Ensure that Mobile Device Management (MDM) profile is installed on your device, if required by company policy. (Source: 001_Setting_Up_a_Mobile_Device_for_Company_Email.txt)
2. Go to the Settings app on your mobile device.
3. Select "Mail" or "Email" (depending on your device's operating system).
4. Tap "Add Account" or "Create a new account".
5. Select "Exchange" or "Corporate" as the account type.
6. Enter your company email address and password.
7. If prompted, enter the company's email server address (e.g., mail.company.com).
8. Select the desired synchronization options.
9. Tap "Save" or "Done" to complete the setup process.

**For Android devices:**

1. Go to the Email app on your Android device.
2. Tap on the "Add account" or "Create a new account" button.
3. Select "Email" or "Corporate" as the account type, depending on your email provider.
4. Enter your email address and password in the required fields.
5. Tap "Next" to proceed.
6. The device will attempt to automatically configure the server settings. If it fails, you will need to enter the settings manually.
7. Tap on "Manual setup" or "Advanced setup" to enter the server settings manually.

Note: If MDM is required, contact your IT department for assistance. (Source: 001_Setting_Up_a_Mobile_Device_for_Company_Email.txt)
```

### Qestion 2: How to reset jammed printer?
```
[-] You: How to reset jammed printer?        

TOP_K Chunk : [4]
================================================================================
source                                                           distance   rank
009_Resetting_a_Jammed_Printer.txt                                 0.2581      1
009_Resetting_a_Jammed_Printer.txt                                 0.4356      2
009_Resetting_a_Jammed_Printer.txt                                 0.5358      3
009_Resetting_a_Jammed_Printer.txt                                 0.5530      4

[+] Assistant: To reset a jammed printer, follow these steps:

1. Turn off the printer (Step 1).
2. Open the printer (Step 2).
3. Identify and remove any obstructions or debris, such as dust or dirt, from the printer (Step 3, [2]).
4. Realign the paper tray if it was dislodged during the jam (Step 5).
5. Check and clean the print head with a lint-free cloth or cotton swab to remove any blockages or dried ink (Step 6).
6. Reassemble the printer in the reverse order of how you disassembled it (Step 7).
7. Power on the printer and test it by printing a test page or a document (Step 8).

Source: 009_Resetting_a_Jammed_Printer.txt

```
### Qestion 3: Help me fix problem with Microsoft Office
```
TOP_K Chunk : [4]
================================================================================
source                                                           distance   rank
004_Troubleshooting_Issues_with_Microsoft_Office.txt               0.3102      1
004_Troubleshooting_Issues_with_Microsoft_Office.txt               0.3736      2
004_Troubleshooting_Issues_with_Microsoft_Office.txt               0.3991      3
004_Troubleshooting_Issues_with_Microsoft_Office.txt               0.4099      4

[+] Assistant: I could not find a specific answer to your question in the provided context. However, based on the steps provided in the article, I can suggest some general troubleshooting steps:

1. Try restarting Microsoft Office to see if the issue resolves.
2. Check for updates and install any available updates.
3. Try resetting Office configuration by following the steps in Step 6 of the article.
4. If none of the above steps resolve the issue, try reinstalling Microsoft Office.

If you could provide more information about the specific problem you are experiencing with Microsoft Office, I may be able to provide more tailored advice.

[1] Source: 004_Troubleshooting_Issues_with_Microsoft_Office.txt
[2] Source: 004_Troubleshooting_Issues_with_Microsoft_Office.txt
[3] Source: 004_Troubleshooting_Issues_with_Microsoft_Office.txt
[4] Source: 004_Troubleshooting_Issues_with_Microsoft_Office.txt

```

## Test with Off-topic Question
### Qestion 4: Tell me about cambodia?
### Qestion 5: What is Information Technology?
```
[-] You: Tell me about cambodia?

TOP_K Chunk : [0]
================================================================================
source                                                           distance   rank

[+] Assistant: I could not find this in your documents.

[-] You: What is Information Technology?

TOP_K Chunk : [0]
================================================================================
source                                                           distance   rank

[+] Assistant: I could not find this in your documents.
```
In conclusion: for off-topic questions, the retriever still returns the top-k nearest chunks by default, since vector search always finds some closest match regardless of relevance. However, the distance values for these off-topic chunks are noticeably higher than for chunks that genuinely answer a question found in the documents — in our tests, ~1.22–1.29 for an irrelevant query versus ~0.29–0.42 for a relevant one.

To handle this, we added a distance threshold (MAX_DISTANCE = 0.8) that filters out any chunk whose distance exceeds this value. Since off-topic queries produce distances well above 0.8, no chunks pass the filter, and retrieve() correctly returns an empty list — allowing the system to report "no relevant information found" instead of returning irrelevant context.