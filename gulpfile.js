import gulp from "gulp";
import tslint from "gulp-tslint";
import ts from "gulp-typescript";
import { deleteAsync } from "del";

gulp.task("clean", () => deleteAsync(["website/build"]));

gulp.task("copy", () => gulp.src(["website/source/**/*", "!website/source/**/*.ts"]).pipe(gulp.dest("website/build")));

gulp.task("ts", function() {
  var client_project = ts.createProject('website/tsconfig.json');
  return gulp.src(["website/source/**/*.ts", "node_modules/types/@types/**/*.d.ts"])
    .pipe(client_project()).js
    .pipe(gulp.dest("website/build"));
});

gulp.task("build", gulp.series(
  "clean",
  "ts",
  "copy",
));
