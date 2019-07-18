#include <DigiUSB.h>
void setup() {
DigiUSB.begin();
DigiUSB.delay(1000);

}
void loop()
{
DigiUSB.println("{\n\t \"P2P\": {\n\t \"Pwd\": \"16digitNo\"\n\t}\n\t \"224.1.1.1\": {\n\t \"Pwd\": \"16digitNo1234567\"\n\t}\n\t \"224.1.1.1\": {\n\t \"Pwd\": \"16digitNo1234567\"\n\t}\n\t \"224.1.1.1\": {\n\t \"Pwd\": \"16digitNo1234567\"\n\t}\n\t \"224.1.1.1\": {\n\t \"Pwd\": \"16digitNo1234567\"\n\t}\n\t \"224.1.1.1\": {\n\t \"Pwd\": \"16digitNo1234567\"\n\t}\n}");
DigiUSB.println("This is property of Indian Govt.");
DigiUSB.delay(5000);
}
