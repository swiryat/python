import java.util.Scanner;
import javax.sound.midi.InvalidMidiDataException;
import javax.sound.midi.MidiSystem;
import javax.sound.midi.MidiUnavailableException;
import javax.sound.midi.Receiver;
import javax.sound.midi.ShortMessage;
import javax.sound.midi.Synthesizer;

public class App {

    private static final byte C = 60; // do
    private static final byte C_SHARP = 61; // do#
    private static final byte D = 62; // re
    private static final byte D_SHARP = 63; // re#
    private static final byte E_FLAT = 63; // mib
    private static final byte E = 64; // mi
    private static final byte F = 65; // fa
    private static final byte F_SHARP = 66; // fa#
    private static final byte G = 67; // sol
    private static final byte G_SHARP = 68; // sol#
    private static final byte A_FLAT = 68; // lab
    private static final byte A = 69; // la
    private static final byte A_SHARP = 70; // la#
    private static final byte B_FLAT = 70; // sib
    private static final byte B = 71; // si

    public static void main(String[] args)
            throws MidiUnavailableException, InvalidMidiDataException, InterruptedException {

        Synthesizer synthesizer = MidiSystem.getSynthesizer();
        synthesizer.open();
        Receiver receiver = synthesizer.getReceiver();

        Scanner scanner = new Scanner(System.in);
        System.out.println("Please enter notes (A-G) without spaces (type 'q' to play): ");
        String input = scanner.nextLine().trim();

        while (!input.equalsIgnoreCase("q")) {
            String[] notes = input.toUpperCase().split("");
            playNotes(receiver, notes);
            System.out.println("Please enter notes (A-G) without spaces (type 'q' to play): ");
            input = scanner.nextLine().trim();
        }

        synthesizer.close();
        scanner.close();
    }

    private static void playNotes(Receiver receiver, String[] notes)
            throws InvalidMidiDataException, InterruptedException {
        ShortMessage msg = new ShortMessage();
        for (String note : notes) {
            switch (note) {
                case "A":
                    playNote(receiver, msg, A);
                    break;
                case "A#":
                case "Bb":
                    playNote(receiver, msg, B_FLAT);
                    break;
                case "B":
                    playNote(receiver, msg, B);
                    break;
                case "C":
                    playNote(receiver, msg, C);
                    break;
                case "C#":
                case "Db":
                    playNote(receiver, msg, C_SHARP);
                    break;
                case "D":
                    playNote(receiver, msg, D);
                    break;
                case "D#":
                case "Eb":
                    playNote(receiver, msg, D_SHARP);
                    break;
                case "E":
                    playNote(receiver, msg, E);
                    break;
                case "F":
                    playNote(receiver, msg, F);
                    break;
                case "F#":
                case "Gb":
                    playNote(receiver, msg, F_SHARP);
                    break;
                case "G":
                    playNote(receiver, msg, G);
                    break;
                case "G#":
                case "Ab":
                    playNote(receiver, msg, G_SHARP);
                    break;
                default:
                    System.out.println("Invalid note: " + note);
            }
        }
    }

    private static void playNote(Receiver receiver, ShortMessage msg, byte note)
            throws InvalidMidiDataException, InterruptedException {
        msg.setMessage(ShortMessage.NOTE_ON, note, 100);
        receiver.send(msg, -1);
        Thread.sleep(500);
        msg.setMessage(ShortMessage.NOTE_OFF, note, 100);
        receiver.send(msg, -1);
    }
}
