import SwiftUI

struct SettingsView: View {
    @State private var volume: Double = UserPreferences.volume
    @State private var metronomeEnabled: Bool = UserPreferences.metronomeEnabled
    @State private var hapticFeedbackEnabled: Bool = UserPreferences.hapticFeedbackEnabled
    
    var body: some View {
        Form {
            Section(header: Text("Audio Settings")) {
                VStack(alignment: .leading) {
                    Text("Volume")
                    Slider(value: $volume, in: 0...1) { _ in
                        UserPreferences.volume = volume
                    }
                }
                
                Toggle("Enable Metronome", isOn: $metronomeEnabled)
                    .onChange(of: metronomeEnabled) { oldValue, newValue in
                        UserPreferences.metronomeEnabled = newValue
                    }
            }
            
            Section(header: Text("Feedback")) {
                Toggle("Haptic Feedback", isOn: $hapticFeedbackEnabled)
                    .onChange(of: hapticFeedbackEnabled) { oldValue, newValue in
                        UserPreferences.hapticFeedbackEnabled = newValue
                    }
            }
            
            Section {
                Button("Reset to Defaults") {
                    UserPreferences.resetToDefaults()
                    volume = UserPreferences.volume
                    metronomeEnabled = UserPreferences.metronomeEnabled
                    hapticFeedbackEnabled = UserPreferences.hapticFeedbackEnabled
                }
                .foregroundColor(.red)
            }
        }
        .navigationTitle("Settings")
    }
} 