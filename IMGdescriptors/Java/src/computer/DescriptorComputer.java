package computer;

import org.opencv.core.Mat;

public abstract class DescriptorComputer {
	public abstract Mat compute(Mat image);
}
