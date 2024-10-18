import {motion} from 'framer-motion';
import {WifiIcon} from 'lucide-react';

function NFCtouchScreen() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-gray-900 to-gray-800 text-white p-4">
            <div className="text-center space-y-8">
            <motion.div
                className="w-24 h-24 mx-auto bg-white/10 rounded-full flex items-center justify-center"
                animate={{
                scale: [1, 1.1, 1],
                opacity: [0.5, 1, 0.5]
                }}
                transition={{
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut"
                }}
            >
                <WifiIcon className="w-12 h-12 text-white" />
            </motion.div>
            <div className="space-y-2">
                <p className="text-2xl font-bold">デバイスをかざしてください</p>
                <p className="text-lg text-gray-300">Please tap your device</p>
            </div>
            </div>
        </div>
    )
}

export default NFCtouchScreen;