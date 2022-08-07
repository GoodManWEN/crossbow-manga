use numpy::ndarray::Array;
use numpy::PyReadonlyArray2;
use pyo3::{pymodule, types::PyModule, PyResult, Python};
use std::collections::VecDeque;

#[pymodule]
fn crossbow_manga_lib(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    
    #[derive(Debug)]
    #[derive(Copy, Clone)]
    struct Point {
        x: isize,
        y: isize
    }

    impl Point {
        fn round8(&self) -> [Point;8] {
            [
                Point{x: self.x-1, y: self.y-1},
                Point{x: self.x-1, y: self.y},
                Point{x: self.x-1, y: self.y+1},
                Point{x: self.x, y: self.y+1},
                Point{x: self.x+1, y: self.y+1},
                Point{x: self.x+1, y: self.y},
                Point{x: self.x+1, y: self.y-1},
                Point{x: self.x, y: self.y-1}
            ]
        }
    }


    #[pyfn(m)]
    fn region_grow<'py>(
        _py: Python<'py>,
        arr: PyReadonlyArray2<i16>,
        targ_arr: PyReadonlyArray2<i16>,
        pos_x: usize,
        pos_y: usize,
        targ_color: i16,
        threshold: i16
    ) -> f64 {
        let arr = unsafe { arr.as_array_mut() };
        let mut targ_arr = unsafe { targ_arr.as_array_mut() };
        let shape = arr.shape();
        let f_y: usize = shape[0];
        let f_x: usize = shape[1];
        let max_y = f_y as isize - 1;
        let max_x = f_x as isize - 1;

        let mut seed_list = VecDeque::from([Point{x: pos_x as isize, y: pos_y as isize},]);
        let mut avg_color: f64 = targ_color as f64;
        let mut avg_color_count: f64 = 1.0;
        
       // First, use the growth algorithm to search for relevant fill-in areas
        while (seed_list.len()) > 0 {
            let t_point = seed_list.pop_front().unwrap();
            targ_arr[(t_point.y as usize, t_point.x as usize)] = 255;
            for t_point_g in t_point.round8() {
                if t_point_g.x < 0 || t_point_g.y < 0 || t_point_g.x > max_x || t_point_g.y > max_y {
                    continue;
                }
                let t_color = arr[(t_point_g.y as usize, t_point_g.x as usize)];
                if (targ_arr[(t_point_g.y as usize, t_point_g.x as usize)] != 255) && (i16::abs(t_color - avg_color as i16) <= threshold) {
                    targ_arr[(t_point_g.y as usize, t_point_g.x as usize)] = 255;
                    seed_list.push_back(t_point_g);
                    // update_avg_color
                    avg_color = (avg_color * avg_color_count + t_color as f64) / (avg_color_count + 1.0);
                    avg_color_count += 1.0;
                }
            }
        }
        
        // The second step is to use the growth algorithm in the new layer to search for unselected parts.
        // Select the unpainted part of the four corners of the image, return fails if all smeared. 
        let f4 = [Point{x:0,y:0}, Point{x:max_x-1,y:0}, Point{x:0,y:max_y-1}, Point{x:max_x, y:max_y}];
        let mut anchor = Point{x:0, y:0};
        for idx in 0..5 {
            if idx == 4 {
                // for corner all white
                for y_idx in 0..(f_y as usize) {
                    for x_idx in 0..(f_x as usize) {
                        targ_arr[(y_idx, x_idx)] = 0;
                    }
                }
                return 0.0;
            }
            // else 
            anchor = f4[idx];
            if arr[(anchor.y as usize, anchor.x as usize)] != 255 {
                break
            }
        }
        // For differentiation, color 127 was used for the second application.
        seed_list.push_back(anchor);
        while (seed_list.len()) > 0 {
            let t_point = seed_list.pop_front().unwrap();
            targ_arr[(t_point.y as usize, t_point.x as usize)] = 127;
            for t_point_g in t_point.round8() {
                if t_point_g.x < 0 || t_point_g.y < 0 || t_point_g.x > max_x || t_point_g.y > max_y {
                    continue;
                }
                let t_color = targ_arr[(t_point_g.y as usize, t_point_g.x as usize)];
                if t_color == 0 {
                    targ_arr[(t_point_g.y as usize, t_point_g.x as usize)] = 127;
                    seed_list.push_back(t_point_g);
                }
            }
        }
        // 
        let mut t_arr = Array::zeros((f_y as usize, f_x as usize));
        for y_idx in 0..(f_y as usize) {
            for x_idx in 0..(f_x as usize) {
                if targ_arr[(y_idx, x_idx)] != 127 {
                    t_arr[(y_idx, x_idx)] = 255;
                }
            }
        }
        // Using a 3*3 convolution kernel blurs the neighborhood ([1, 1, 1, 1, 0, 1, 1, 1, 1]),
        // smoothing lines while shrinking the selected area slightly
        for y_idx in 0..(f_y as usize) {
            for x_idx in 0..(f_x as usize) {
                let mut summ = 0;
                let mut count = 0;
                let p = Point{x:x_idx as isize, y:y_idx as isize};
                for t_point_g in p.round8() {
                    if t_point_g.x < 0 || t_point_g.y < 0 || t_point_g.x > max_x || t_point_g.y > max_y {
                        continue;
                    } else {
                        summ += t_arr[(t_point_g.y as usize, t_point_g.x as usize)];
                        count += 1;
                    }
                }
                targ_arr[(y_idx, x_idx)] = summ/count;
            }
        }
        // Perform color toning, binarize partition line 200
        for y_idx in 0..(f_y as usize) {
            for x_idx in 0..(f_x as usize) {
                if targ_arr[(y_idx, x_idx)] < 200 {
                    targ_arr[(y_idx, x_idx)] = 0;
                } else {
                    targ_arr[(y_idx, x_idx)] = 255;
                }
            }
        }
        avg_color
    }
    Ok(())
}
