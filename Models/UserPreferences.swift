import Foundation

struct UserPreferences {
    // Keys for UserDefaults
    private enum Keys {
        static let lastShotType = "lastShotType"
        static let lastPro = "lastPro"
        static let volume = "volume"
        static let metronomeEnabled = "metronomeEnabled"
        static let hapticFeedbackEnabled = "hapticFeedbackEnabled"
    }
    
    // Default values
    private static let defaults: [String: Any] = [
        Keys.volume: 0.8,
        Keys.metronomeEnabled: true,
        Keys.hapticFeedbackEnabled: true
    ]
    
    // MARK: - Properties
    
    static var lastShotType: String? {
        get { UserDefaults.standard.string(forKey: Keys.lastShotType) }
        set { UserDefaults.standard.set(newValue, forKey: Keys.lastShotType) }
    }
    
    static var lastPro: String? {
        get { UserDefaults.standard.string(forKey: Keys.lastPro) }
        set { UserDefaults.standard.set(newValue, forKey: Keys.lastPro) }
    }
    
    static var volume: Double {
        get { UserDefaults.standard.double(forKey: Keys.volume) }
        set { UserDefaults.standard.set(newValue, forKey: Keys.volume) }
    }
    
    static var metronomeEnabled: Bool {
        get { UserDefaults.standard.bool(forKey: Keys.metronomeEnabled) }
        set { UserDefaults.standard.set(newValue, forKey: Keys.metronomeEnabled) }
    }
    
    static var hapticFeedbackEnabled: Bool {
        get { UserDefaults.standard.bool(forKey: Keys.hapticFeedbackEnabled) }
        set { UserDefaults.standard.set(newValue, forKey: Keys.hapticFeedbackEnabled) }
    }
    
    // MARK: - Methods
    
    static func registerDefaults() {
        UserDefaults.standard.register(defaults: defaults)
    }
    
    static func resetToDefaults() {
        lastShotType = nil
        lastPro = nil
        volume = defaults[Keys.volume] as? Double ?? 0.8
        metronomeEnabled = defaults[Keys.metronomeEnabled] as? Bool ?? true
        hapticFeedbackEnabled = defaults[Keys.hapticFeedbackEnabled] as? Bool ?? true
    }
} 